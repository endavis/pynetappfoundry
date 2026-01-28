# PyNetAppFoundry Code Review & Improvement Plan

## Executive Summary

This is a NetApp ONTAP administration library with CLI (`nf`). While well-structured for a "personal playground," it has several areas needing attention before being production-ready.

---

## Critical Issues (Priority 1)

### 1. ✅ Security: SSL Verification Disabled
**Location:** `src/pynetappfoundry/clients/openapi.py:369`
```python
resp = self.session.request(..., verify=False)  # MITM vulnerability
```
**Fix:** Make SSL verification configurable, default to `True`.

**Status:** Completed in PR #8. Added `verify_ssl` parameter (default: `True`).

### 2. ✅ Security: SQL Injection Risk
**Location:** `src/pynetappfoundry/db/metrics.py:40-43, 46-58, 71-76, 92-96`
```python
cur.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}"')
```
**Risk:** While table names are "code-controlled," this pattern is fragile.
**Fix:** Use parameterized queries or validate table names against allowlist.

**Status:** Completed in PR #8. Added `_validate_table_name()` with regex validation.

### 3. ✅ Minimal Test Coverage
**Current state:** Only 1 test file exists (`tests/unit/test_size_utils.py`)
**Impact:** No confidence in refactoring; regressions likely.
**Fix:** Add tests for core modules (Config, APIWrapper, database classes).

**Status:** Completed in PR #8. Added 90 tests:
- `tests/unit/test_config.py` (32 tests)
- `tests/unit/test_openapi.py` (42 tests)
- `tests/unit/test_db.py` (16 tests)

---

## High Priority Issues (Priority 2)

### 4. ✅ Documentation Mismatch
**Location:** `docs/usage/basics.md` vs actual implementation
- Docs say JSON configs in `~/.config/pynetappfoundry/`
- Code uses TOML files in relative `config/` directory
**Fix:** Rewrite docs to match actual TOML-based config system.

**Status:** Completed in PR #8. Rewrote `docs/usage/basics.md` to match TOML config.

### 5. ✅ No Type Safety in Models
**Current:** Plain `dict[str, Any]` everywhere
```python
self.data: dict[str, dict[str, dict[str, Any]]] = {}
```
**Impact:** Runtime KeyError crashes, no IDE support, hard to understand data shapes.
**Fix:** Create Pydantic models or TypedDicts for:
- Cluster configuration
- User credentials
- Settings schema
- API responses

**Status:** Completed in PR #14. Added Pydantic models for all resource and settings types.

### 6. ✅ Tight Coupling in Config Access
**Location:** Throughout codebase
```python
# Direct config access with KeyError risk
self.settings["users"][utype]["user"]  # config.py:160
config.settings["ontapapi"]["general"]["base_api_path"]  # ontap/api.py:41
```
**Fix:** Add accessor methods with clear error messages.

**Status:** Completed in PR #16. Added accessor methods to Config class.

---

## Medium Priority Issues (Priority 3)

### 7. OpenAPI Implementation Limitations

**Current approach:** Custom minimal wrapper with:
- No response validation
- No retry logic
- No async support
- Basic reference resolution (no circular ref handling)
- Only JSON content type support

**Should you switch to openapi-core?**

| Aspect | Current APIWrapper | openapi-core |
|--------|-------------------|--------------|
| OpenAPI version | 2.0 (Swagger) | 3.0, 3.1 only |
| Request validation | Yes (jsonschema) | Yes (built-in) |
| Response validation | No | Yes |
| Framework integrations | None | requests, Django, Flask |
| Learning curve | Already known | New library |
| Maintenance | You maintain | Community maintained |

**Findings from spec files:**
- `example-config/apis/ontap/all.json` → **Swagger 2.0** (has `basePath`, no `openapi` field)
- `example-config/apis/dii/all.json` → **OpenAPI 3.x** (has `components` structure)

**Recommendation: Keep current APIWrapper** but enhance it:
- openapi-core won't work for ONTAP without converting specs
- Add response validation using jsonschema
- ✅ Add configurable SSL verification (completed in PR #8)
- Add retry logic with exponential backoff

### 8. ✅ Config Schema Not Documented
**Issue:** Config format is "dynamic" - only way to know valid keys is reading code.
**Fix:** Create a config schema document or JSON Schema for validation.

**Status:** Completed in PR #18. Added `docs/reference/config-schema.md` with comprehensive documentation.

### 9. ✅ Mixed ONTAP Access Patterns
The codebase uses THREE different approaches:
1. `APIWrapper` for REST API (custom)
2. `ONTAPCLI` for SSH CLI (Paramiko)
3. `netapp_ontap` SDK (in some commands like `locks.py`)

**Impact:** Inconsistent patterns, maintenance burden.
**Fix:** Document when to use each; consider consolidating.

**Status:** Completed in PR #20. Added `docs/usage/ontap-access-patterns.md` with decision matrix and usage guide.

---

## Suggested Improvements (Priority 4)

### 10. ✅ Code Quality
- [x] Add `sys.exit(1)` -> raise proper exceptions in `Config.get_user()` *(PR #8)*
- [x] Remove hardcoded key order in `find_closest()` *(PR #26)*
- [x] Add retry logic to API calls *(PR #24)*
- [x] Make timeout configurable per-client *(PR #28)*

### 11. ✅ User Experience
- [x] Better error messages when config keys missing *(PR #16)*
- [x] Add `nf config validate` command *(PR #22)*
- [x] Add `nf config show` to display loaded configuration *(PR #22)*
- [x] Support environment variables for credentials *(PR #22)*

### 12. ✅ Developer Experience
- [x] Add typing stubs or Pydantic models *(PR #14)*
- [x] Add integration test examples *(PR #30)*
- [x] Document the scripting API with more examples *(PR #30)*

---

## Implementation Plan

Based on user preferences: **Testing first**, **Breaking changes OK**, **Keep current OpenAPI wrapper**.

### Phase 1: Testing Foundation ✅
Add comprehensive tests to enable safe refactoring:

1. ✅ **Config tests** (`tests/unit/test_config.py`)
   - Test TOML parsing and data loading
   - Test search functionality (`search()`, `find_closest()`)
   - Test credential retrieval (`get_user()`)

2. ✅ **APIWrapper tests** (`tests/unit/test_openapi.py`)
   - Test reference resolution
   - Test path formatting
   - Test body validation
   - Mock HTTP responses

3. ✅ **Database tests** (`tests/unit/test_db.py`)
   - Test MetricDB operations
   - Test AzEventsDB operations

### Phase 2: Security Fixes ✅
4. ✅ **SSL verification** - Make configurable in `APIWrapper`
5. ✅ **SQL safety** - Validate table names against allowlist

### Phase 3: Documentation ✅
6. ✅ **Config schema documentation** - Document all TOML keys and structure (PR #18)
7. ✅ **Fix `docs/usage/basics.md`** - Align with actual TOML-based system

### Phase 4: Type Safety & Error Handling ✅
8. ✅ **Pydantic models** for cluster, user, settings (PR #14)
9. ✅ **Replace `sys.exit(1)`** with proper exceptions (`ConfigurationError`)

---

## Key Files Modified

| File | Changes | Status |
|------|---------|--------|
| `tests/unit/test_config.py` | Create - Config class tests | ✅ PR #8 |
| `tests/unit/test_openapi.py` | Create - APIWrapper tests | ✅ PR #8 |
| `tests/unit/test_db.py` | Create - Database tests | ✅ PR #8 |
| `src/pynetappfoundry/clients/openapi.py` | Make `verify` configurable | ✅ PR #8 |
| `src/pynetappfoundry/db/metrics.py` | Add table name validation | ✅ PR #8 |
| `src/pynetappfoundry/core/config.py` | Replace sys.exit with exceptions | ✅ PR #8 |
| `docs/usage/basics.md` | Rewrite to match TOML config | ✅ PR #8 |

---

## Verification Plan

After each phase:
1. Run `doit check` to ensure tests pass
2. Run `doit lint` to ensure code quality
3. Manual test: `nf --help` and basic commands still work

---

## Completed PRs

| PR | Description | Issues Closed |
|----|-------------|---------------|
| #8 | Code quality, testing, and security improvements | #7 |
| #10 | Fix _version.py tracking | #9 |
| #12 | Fix griffe workflow | #11 |
| #14 | Add Pydantic models for type-safe configuration | #13 |
| #16 | Add Config accessor methods to reduce tight coupling | #15 |
| #18 | Add comprehensive config schema documentation | #17 |
| #20 | Document ONTAP access patterns | #19 |
| #22 | Add config CLI commands and environment variable support | #21 |
