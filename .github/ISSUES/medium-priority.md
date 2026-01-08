# Medium Priority: Code Quality & Security Improvements

## Medium Priority Issues

These issues improve code quality, maintainability, and address moderate security concerns.

### 1. No README Documentation

**Issue:** The project has no README.md file explaining installation, configuration, or usage.

**Fix:** Create comprehensive README.md with:
- Project description
- Installation instructions
- Configuration guide (environment variables)
- Usage examples
- Architecture overview

---

### 2. Zero Test Coverage

**Issue:** All 27 functions lack unit tests. No test framework installed.

**Fix:**
- Add `pytest` to requirements.txt
- Create `tests/` directory
- Write unit tests for all modules, prioritizing:
  - `processor/classifier.py` (pure functions, easy to test)
  - `utils/helpers.py` (utility functions)
  - `utils/formatter.py` (output formatting)

---

### 3. No Dependency Version Pinning

**Issue:** `requirements.txt` has no version constraints, risking breaking changes.

**Fix:** Pin versions:
```
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
imaplib2>=3.0.0
openai>=1.0.0
python-dotenv>=1.0.0
```

---

### 4. Hardcoded Email Limit

**Location:** `fetcher/fetch_emails.py:61`

```python
for uid in uids[:5]:  # Should use EMAIL_LIMIT config
```

**Fix:** Use the `EMAIL_LIMIT` configuration variable from `utils/config.py`.

---

### 5. Generic Exception Handling

**Locations:** Multiple files catch broad `Exception` instead of specific types.

**Fix:** Use specific exception types (e.g., `imaplib.IMAP4.error`, `openai.APIError`).

---

### 6. IMAP Folder Name Validation

**Location:** `fetcher/imap_actions.py:9, 13`

**Issue:** `target_folder` parameter passed to IMAP commands without validation.

**Fix:** Validate folder names against allowed characters/patterns.

---

### 7. JSON Schema Validation Missing

**Location:** `utils/config.py:14-19`

**Issue:** `OTHER_ACCOUNTS_JSON` parsed without schema validation.

**Fix:** Add schema validation for required fields (username, password, imap_server).

---

### 8. Overly Strict Content Validation

**Location:** `utils/helpers.py:23-36`

**Issue:** Blocks legitimate emails containing words like "password reset" or "key conference".

**Fix:** Improve pattern matching to avoid false positives.

---

## Acceptance Criteria

- [ ] Create README.md with full documentation
- [ ] Add pytest and create test suite
- [ ] Pin dependency versions
- [ ] Use EMAIL_LIMIT config variable
- [ ] Replace generic exception handling
- [ ] Add IMAP folder validation
- [ ] Add JSON schema validation
- [ ] Improve content validation patterns

---

**Labels:** `enhancement`, `documentation`, `testing`
