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
import sys
import tomllib
from pathlib import Path
from typing import Any

_file_name = Path(__file__).name


class Config:
    """Configuration manager for TOML-based config files."""

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
            output_dir: Directory for output files. If empty, uses data/{script_name}/output.
            script_name: Name of the calling script (used for directory naming).
            args: Optional parsed arguments object.
        """
        self.data: dict[str, dict[str, dict[str, Any]]] = {}
        self.args = args
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

    def get_user(self, utype: str = "clusters", uobject: str = "") -> tuple[str, str]:
        """Get user credentials for a given type and object.

        Args:
            utype: Type of object (e.g., 'clusters').
            uobject: Name of the specific object.

        Returns:
            Tuple of (username, encoded_password).

        Raises:
            SystemExit: If credentials cannot be found.
        """
        user: str | None = None
        enc: str | None = None

        try:
            user = self.settings["users"][utype]["user"]
            enc = self.settings["users"][utype]["enc"]
        except KeyError:
            pass

        try:
            user = self.data[utype][uobject]["user"]
            enc = self.data[utype][uobject]["enc"]
        except KeyError:
            pass

        if not user:
            logging.error(f"Could not find user for {utype} and {uobject}")
            sys.exit(1)
        if not enc:
            logging.error(f"Could not find password for {utype} and {uobject}")
            sys.exit(1)

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

    def load_data(self, data: dict[str, Any]) -> None:
        """Load data sections from a parsed TOML.

        Args:
            data: Parsed TOML data dictionary.
        """
        for data_type in self.data_types:
            if data_type not in self.data:
                self.data[data_type] = {}
            if data_type in data:
                logging.debug(
                    f"{_file_name} : adding {len(data[data_type])} {data_type} items"
                )
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

    def search(
        self, data_type: str, search_dict: dict[str, str]
    ) -> dict[str, dict[str, Any]]:
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
                        f"{_file_name} :      search: {key} not"
                        " in item details, did not match"
                    )
                    break
                logging.debug(
                    f"{_file_name} :      search: check_term {search_dict[key]}, "
                    f"{item_details[key]} returned "
                    f"{self.check_term(search_dict[key], item_details[key])}"
                )
                result_check.append(
                    self.check_term(search_dict[key], item_details[key])
                )

            if all(result_check):
                logging.debug(
                    f"{_file_name} :      search: item - {item_details['name']} matched"
                )
                results[item] = item_details
            else:
                logging.debug(
                    f"{_file_name} :      search: item - {item_details['name']} "
                    "did not match"
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

    def find_closest(
        self, data_type: str, tree: dict[str, str]
    ) -> dict[str, Any] | None:
        """Find the closest matching item by progressively relaxing search criteria.

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
        key_order = ["div", "bu", "app", "env", "subapp", "cloud", "region"]
        key_order.reverse()
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
                    logging.debug(
                        f"{_file_name} :  removing {key} and searching {tree = }"
                    )
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
