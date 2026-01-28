"""Module to read configs and setup environment.

# return any items match all 3 tags
-f '{"bu":"Business", "env":"Prod", "tags":"active"}'
# return any item that matches bu and env and has both 'active' and 'workload' as a tag
-f '{"bu":"Business", "env":"Prod", "tags":"active && workload"}'
# return any item that matches bu, env, and tags and
#            app is one of app_name1 or app_name2
-f '{"bu":"Business", "app": "app_name1 || app_name2", "env":"Prod", "tags":"active"}'
# return any items with either name1 or name2
-f '{"name":"name1 || name2"}'

a data toml has the following section:
[settings]
type='data'

the following sections are valid in a data toml:
[aiquims]
[connectors]
[clusters]
[cloudinsights]
[azure]
[ibm]

This data is loaded into the Config.data attribute

And there are several ways to group this data into tomls:
1) A specific toml for each type of data
2) a toml for each distinct unit, like division, or bu

In addition, there are specific tomls
Azure settings (azure.toml)
IBM/Softlayer settings (ibm.toml)
AWS settings (aws.toml)
global settings (settings.toml)

These tomls are loading into the Config.config
    attribute by file name (without the .toml)
"""

from __future__ import annotations

import logging
import os
import tomllib
from pathlib import Path
from typing import Any, TypeVar

from pynetappfoundry.core.models import (
    DIIAPISettings,
    LicensingSettings,
    ONTAPAPISettings,
    SMTPSettings,
)

_file_name = Path(__file__).name

T = TypeVar("T")


class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""

    pass


class Config:
    """Configuration manager for TOML-based config files.

    Environment Variables:
        NF_CONFIG_DIR: Override the default config directory path.
        NF_<CLUSTER>_USER: Override username for a specific cluster.
        NF_<CLUSTER>_PASSWORD: Override password (base64 encoded) for a specific cluster.

    The cluster name in environment variables should be uppercase with hyphens
    replaced by underscores (e.g., cluster-prod -> NF_CLUSTER_PROD_USER).
    """

    def __init__(
        self,
        config_dir: str | Path = "config",
        output_dir: str | Path = "",
        script_name: str = "",
        args: Any = None,
    ) -> None:
        """Initialize the configuration manager.

        Args:
            config_dir: Directory containing config files (relative to cwd or absolute).
                        Can be overridden by NF_CONFIG_DIR environment variable.
            output_dir: Directory for output files. If empty, uses data/{script_name}/output.
            script_name: Name of the calling script (used for directory naming).
            args: Optional parsed arguments object.
        """
        self.data: dict[str, dict[str, dict[str, Any]]] = {}
        self.args = args
        # Check for environment variable override
        env_config_dir = os.environ.get("NF_CONFIG_DIR")
        if env_config_dir:
            logging.debug(f"Using config dir from NF_CONFIG_DIR: {env_config_dir}")
            config_dir = env_config_dir
        self.config_dir = Path.cwd() / config_dir
        self.data_types = ["aiqums", "connectors", "cloudinsights", "clusters", "azure"]
        self.settings: dict[str, Any] = {}
        self.parse_data()
        logging.debug(f"Toplevel settings: {list(self.settings.keys())}")
        self.script_name = script_name
        self.data_dir = Path(os.getcwd()) / "data" / script_name

        if output_dir:
            self.output_dir = Path(output_dir)
            self.db_dir = Path(output_dir)
        else:
            self.output_dir = self.data_dir / "output"
            self.db_dir = self.data_dir / "db"

        self.files_dir = self.data_dir / "files"
        self.log_dir = self.data_dir / "logs"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.files_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.db_dir, exist_ok=True)

    def get_schema_location(self, api_name: str) -> Path:
        """Get the path to API schema files.

        Args:
            api_name: Name of the API (e.g., 'ontap', 'dii').

        Returns:
            Path to the API schema directory.
        """
        return Path(self.config_dir / "apis" / api_name)

    def get_setting(self, *keys: str, default: T | None = None) -> Any | T | None:
        """Get a nested setting value with a clear error message if not found.

        This method provides safe access to nested configuration values,
        avoiding KeyError exceptions with unhelpful messages.

        Args:
            *keys: Sequence of keys to traverse (e.g., 'ontapapi', 'general', 'base_api_path').
            default: Value to return if the key path doesn't exist. If None and key is missing,
                     raises ConfigurationError.

        Returns:
            The value at the specified key path, or the default value.

        Raises:
            ConfigurationError: If the key path doesn't exist and no default is provided.

        Example:
            >>> config.get_setting('ontapapi', 'general', 'base_api_path')
            '/api'
            >>> config.get_setting('missing', 'key', default='/default')
            '/default'
        """
        current: Any = self.settings
        path_so_far: list[str] = []

        for key in keys:
            path_so_far.append(key)
            if not isinstance(current, dict):
                if default is not None:
                    return default
                raise ConfigurationError(
                    f"Cannot access '{key}' in non-dict value at "
                    f"'{'.'.join(path_so_far[:-1])}'. "
                    "Check your configuration files."
                )
            if key not in current:
                if default is not None:
                    return default
                raise ConfigurationError(
                    f"Missing configuration key '{'.'.join(path_so_far)}'. "
                    f"Available keys at '{'.'.join(path_so_far[:-1]) or 'root'}': "
                    f"{list(current.keys())}. "
                    "Check your configuration files."
                )
            current = current[key]

        return current

    def get_smtp_settings(self) -> SMTPSettings:
        """Get SMTP settings for sending emails.

        Returns:
            SMTPSettings object with server configuration.

        Raises:
            ConfigurationError: If SMTP settings are not configured.
        """
        try:
            smtp_data = self.get_setting("settings", "SMTP")
            return SMTPSettings.model_validate(smtp_data)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid SMTP configuration: {e}. "
                "Ensure settings.toml has a valid [settings.SMTP] section with "
                "'server', 'port', 'user', 'password', and 'auth' fields."
            ) from e

    def get_ontap_api_settings(self) -> ONTAPAPISettings:
        """Get ONTAP REST API settings.

        Returns:
            ONTAPAPISettings object with API configuration.

        Raises:
            ConfigurationError: If ONTAP API settings are not configured.
        """
        try:
            ontap_data = self.get_setting("ontapapi", "general")
            return ONTAPAPISettings.model_validate(ontap_data)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid ONTAP API configuration: {e}. "
                "Ensure settings.toml has a valid [ontapapi.general] section "
                "with 'base_api_path' field."
            ) from e

    def get_dii_api_settings(self) -> DIIAPISettings:
        """Get Data Infrastructure Insights API settings.

        Returns:
            DIIAPISettings object with API configuration.

        Raises:
            ConfigurationError: If DII API settings are not configured.
        """
        try:
            dii_data = self.get_setting("diiapi", "general")
            return DIIAPISettings.model_validate(dii_data)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid DII API configuration: {e}. "
                "Ensure settings.toml has a valid [diiapi.general] section with "
                "'api_ro_token', 'base_url', and 'base_api_path' fields."
            ) from e

    def get_licensing_settings(self) -> LicensingSettings | None:
        """Get licensing notification settings.

        Returns:
            LicensingSettings object if configured, None otherwise.
        """
        try:
            licensing_data = self.get_setting("settings", "licensing")
            return LicensingSettings.model_validate(licensing_data)
        except ConfigurationError:
            return None
        except Exception as e:
            logging.warning(f"Invalid licensing configuration: {e}")
            return None

    def parse_data(self) -> None:
        """Parse all TOML files in the config directory."""
        all_tomls = self.config_dir.rglob("*.toml")
        loaded_tomls: list[Path] = []
        for file in all_tomls:
            logging.debug(f"{_file_name} : parsing {file}")
            self.parse_toml(file)
            loaded_tomls.append(file)

        logging.debug(
            f"{_file_name} :loaded the"
            f" following files: {', '.join([str(path) for path in loaded_tomls])}"
        )
        self.add_searchable_keys()

    def parse_toml(self, file: Path) -> None:
        """Parse a single TOML file.

        Args:
            file: Path to the TOML file.
        """
        with open(file, "rb") as f:
            data = tomllib.load(f)
            if (
                "settings" in data
                and "type" in data["settings"]
                and data["settings"]["type"] == "data"
            ):
                logging.debug(f"{_file_name} : data file: {file.stem}")
                self.load_data(data)
            else:
                logging.debug(f"{_file_name} : config file: {file.stem}")
                if file.stem not in self.settings:
                    self.settings[file.stem] = data
                else:
                    self.settings[file.stem].update(data)

    def _get_env_var_name(self, object_name: str) -> str:
        """Convert object name to environment variable format.

        Args:
            object_name: Name of the object (e.g., 'cluster-prod').

        Returns:
            Environment variable prefix (e.g., 'NF_CLUSTER_PROD').
        """
        # Replace hyphens with underscores and convert to uppercase
        return "NF_" + object_name.replace("-", "_").upper()

    def get_user(self, utype: str = "clusters", uobject: str = "") -> tuple[str, str]:
        """Get user credentials for a given type and object.

        Credentials are resolved in the following order (first found wins):
        1. Environment variables: NF_<OBJECT>_USER and NF_<OBJECT>_PASSWORD
        2. Object-specific config in data files (e.g., clusters.toml)
        3. Default credentials in users.toml for the type

        Args:
            utype: Type of object (e.g., 'clusters').
            uobject: Name of the specific object.

        Returns:
            Tuple of (username, encoded_password).

        Raises:
            ConfigurationError: If credentials cannot be found.
        """
        user: str | None = None
        enc: str | None = None

        # 1. Check environment variables first (highest priority)
        if uobject:
            env_prefix = self._get_env_var_name(uobject)
            env_user = os.environ.get(f"{env_prefix}_USER")
            env_password = os.environ.get(f"{env_prefix}_PASSWORD")
            if env_user:
                logging.debug(f"Using user from {env_prefix}_USER")
                user = env_user
            if env_password:
                logging.debug(f"Using password from {env_prefix}_PASSWORD")
                enc = env_password

        # 2. Check object-specific config (if not already set by env vars)
        if not user or not enc:
            try:
                if not user:
                    user = self.data[utype][uobject]["user"]
                if not enc:
                    enc = self.data[utype][uobject]["enc"]
            except KeyError:
                pass

        # 3. Fall back to default credentials for the type
        if not user or not enc:
            try:
                if not user:
                    user = self.settings["users"][utype]["user"]
                if not enc:
                    enc = self.settings["users"][utype]["enc"]
            except KeyError:
                pass

        if not user:
            logging.error(f"Could not find user for {utype} and {uobject}")
            env_prefix = self._get_env_var_name(uobject) if uobject else "NF_<OBJECT>"
            raise ConfigurationError(
                f"Could not find user for type={utype!r}, object={uobject!r}. "
                f"Set {env_prefix}_USER environment variable, or configure in "
                "users.toml or the object's data file."
            )
        if not enc:
            logging.error(f"Could not find password for {utype} and {uobject}")
            env_prefix = self._get_env_var_name(uobject) if uobject else "NF_<OBJECT>"
            raise ConfigurationError(
                f"Could not find password for type={utype!r}, object={uobject!r}. "
                f"Set {env_prefix}_PASSWORD environment variable (base64 encoded), "
                "or configure 'enc' in config files."
            )

        return user, enc

    def count(self, section: str, id_field: str = "name") -> int:
        """Count unique items in a section.

        Args:
            section: The data section to count.
            id_field: The field to use for uniqueness.

        Returns:
            Number of unique items.
        """
        found: list[Any] = []
        for item in self.data[section]:
            try:
                found.append(getattr(item, id_field))
            except AttributeError:
                found.append(self.data[section][item][id_field])
        return len(set(found))

    def add_searchable_keys(self) -> None:
        """Add default searchable keys to data items."""
        for data_type in self.data_types:
            if (
                data_type in self.settings.get("settings", {})
                and "searchable_keys" in self.settings["settings"][data_type]
            ):
                default_keys = self.settings["settings"][data_type]["searchable_keys"]
                for item in self.data.get(data_type, {}):
                    if "name" not in self.data[data_type][item]:
                        self.data[data_type][item]["name"] = item
                    for key in default_keys:
                        if key not in self.data[data_type][item]:
                            self.data[data_type][item][key] = ""

    def get_relaxation_order(self, data_type: str) -> list[str]:
        """Get the key relaxation order for find_closest searches.

        The relaxation order determines which keys to remove first when
        progressively relaxing search criteria in find_closest().

        Priority:
        1. Explicit 'relaxation_order' in settings for the data type
        2. Reverse of 'searchable_keys' for the data type
        3. Default fallback order

        Args:
            data_type: The data type to get relaxation order for.

        Returns:
            List of keys in order of relaxation (first key removed first).
        """
        default_order = ["region", "subapp", "cloud", "env", "app", "bu", "div"]
        settings = self.settings.get("settings", {}).get(data_type, {})

        # Check for explicit relaxation_order
        if "relaxation_order" in settings:
            return list(settings["relaxation_order"])

        # Fall back to reverse of searchable_keys
        if "searchable_keys" in settings:
            return list(reversed(settings["searchable_keys"]))

        return default_order

    def load_data(self, data: dict[str, Any]) -> None:
        """Load data sections from a parsed TOML.

        Args:
            data: Parsed TOML data dictionary.
        """
        for data_type in self.data_types:
            if data_type not in self.data:
                self.data[data_type] = {}
            if data_type in data:
                logging.debug(f"{_file_name} : adding {len(data[data_type])} {data_type} items")
                self.data[data_type].update(data[data_type])

    def chk_and(self, search_term: str, values: list[str] | str) -> bool:
        """Check if an && (AND) condition matches.

        Args:
            search_term: Search term with && operators.
            values: Values to check against.

        Returns:
            True if all terms match.
        """
        # && only makes sense for lists
        if not isinstance(values, list):
            return False
        terms = [item.strip() for item in search_term.split(" && ")]
        return set(terms).issubset(values)

    def chk_or(self, search_term: str, value: list[str] | str) -> bool:
        """Check if an || (OR) condition matches.

        Args:
            search_term: Search term with || operators.
            value: Value to check against.

        Returns:
            True if any term matches.
        """
        terms = [item.strip() for item in search_term.split(" || ")]
        if isinstance(value, list):
            return any(item in value for item in terms)
        else:
            return any(item == value for item in terms)

    def check_term(self, term: str, value: list[str] | str) -> bool:
        """Check if a search term matches a value.

        Args:
            term: Search term (may contain && or ||).
            value: Value to check against.

        Returns:
            True if the term matches.
        """
        if " || " in term:
            return self.chk_or(term, value)
        elif " && " in term:
            return self.chk_and(term, value)
        else:
            if isinstance(value, list):
                return term in value
            else:
                return term == value

    def search(self, data_type: str, search_dict: dict[str, str]) -> dict[str, dict[str, Any]]:
        """Search for items that match the given fields.

        Each param should be a dictionary with field and value.
        This is case insensitive.

        Value can be {'tags':'active && Workload'} or
                     {'app': 'App1 || App2'}

        Args:
            data_type: Type of data to search (e.g., 'clusters').
            search_dict: Dictionary of field/value pairs to match.

        Returns:
            Dictionary of matching items.
        """
        if not search_dict:
            return self.data[data_type].copy()
        logging.debug(f"{_file_name} :    search:")
        logging.debug(f"{_file_name} :     {data_type = }")
        logging.debug(f"{_file_name} :     {search_dict = }")
        results: dict[str, dict[str, Any]] = {}
        for item in self.data[data_type]:
            item_details = self.data[data_type][item]
            logging.debug(f"{_file_name} :      search: item - {item_details['name']}")
            result_check: list[bool] = []
            for key in search_dict:
                logging.debug(f"{_file_name} :      search: checking {key}")
                if key not in item_details:
                    result_check.append(False)
                    logging.debug(
                        f"{_file_name} :      search: {key} not in item details, did not match"
                    )
                    break
                logging.debug(
                    f"{_file_name} :      search: check_term {search_dict[key]}, "
                    f"{item_details[key]} returned "
                    f"{self.check_term(search_dict[key], item_details[key])}"
                )
                result_check.append(self.check_term(search_dict[key], item_details[key]))

            if all(result_check):
                logging.debug(f"{_file_name} :      search: item - {item_details['name']} matched")
                results[item] = item_details
            else:
                logging.debug(
                    f"{_file_name} :      search: item - {item_details['name']} did not match"
                )

        logging.debug(f"{_file_name} : search returned - {list(results.keys())}")
        return results

    def get_clusters(self, search_terms: dict[str, str]) -> dict[str, dict[str, Any]]:
        """Get clusters matching search terms.

        Args:
            search_terms: Dictionary of field/value pairs to match.

        Returns:
            Dictionary of matching clusters.
        """
        return self.search("clusters", search_terms)

    def find_closest(self, data_type: str, tree: dict[str, str]) -> dict[str, Any] | None:
        """Find the closest matching item by progressively relaxing search criteria.

        The order in which keys are relaxed (removed) is determined by:
        1. Explicit 'relaxation_order' in settings for the data type
        2. Reverse of 'searchable_keys' for the data type
        3. Default fallback order

        Args:
            data_type: Type of data to search.
            tree: Dictionary of hierarchical search criteria.

        Returns:
            The closest matching item, or None if not found.
        """
        logging.debug(f"{_file_name} :find_closest")
        logging.debug(f"{_file_name} :  {data_type = }")
        logging.debug(f"{_file_name} :  {tree = }")
        tree = tree.copy()
        key_order = self.get_relaxation_order(data_type)
        found: dict[str, Any] | None = None

        # remove empty keys
        for key in key_order:
            if key in tree and tree[key] == "":
                del tree[key]

        logging.debug(f"{_file_name} :  initial search {tree = }")
        # try matching tree as is
        results = self.search(data_type, tree)
        if len(results) == 1:
            found = results.popitem()[1]

        else:
            # go through the key_order and delete keys until something is found
            for key in key_order:
                if key in tree:
                    logging.debug(f"{_file_name} :  removing {key} and searching {tree = }")
                    del tree[key]
                else:
                    continue
                if tree:
                    results = self.search(data_type, tree)
                    logging.debug(f"{_file_name} :  search_returned {results}")
                    if len(results) == 1:
                        found = results.popitem()[1]
                        break

        logging.debug(f"{_file_name} : find_closest - {found = }")
        return found
