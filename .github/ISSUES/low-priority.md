# Low Priority: Best Practices & Enhancements

## Low Priority Issues

These issues represent best practices and enhancements for long-term maintainability.

### 1. Add Type Hints Consistently

**Issue:** Type hints are used inconsistently across modules.

**Fix:** Add type hints to all function signatures:
```python
def classify_email(email_obj: Dict[str, str]) -> str:
def fetch_emails(imap_conn: Optional[IMAP4_SSL] = None, ...) -> List[Dict]:
```

---

### 2. Add CI/CD Pipeline

**Issue:** No automated testing or linting on commits/PRs.

**Fix:** Create `.github/workflows/ci.yml` with:
- Python linting (flake8/ruff)
- Type checking (mypy)
- Unit tests (pytest)
- Security scanning (bandit)

---

### 3. Add CONTRIBUTING.md

**Issue:** No contribution guidelines for external contributors.

**Fix:** Create CONTRIBUTING.md with:
- Development setup
- Code style guidelines
- PR process
- Testing requirements

---

### 4. Add CHANGELOG.md

**Issue:** No change history tracking.

**Fix:** Create CHANGELOG.md following Keep a Changelog format.

---

### 5. Duplicate Import Cleanup

**Location:** `scripts/test_imap.py:2,4`

```python
import os          # Line 2
from dotenv import load_dotenv
import os          # Line 4 - DUPLICATE
```

**Fix:** Remove duplicate import.

---

### 6. Consider Secrets Manager

**Issue:** Sensitive credentials stored in environment variables.

**Enhancement:** Consider using a secrets manager (AWS Secrets Manager, HashiCorp Vault, or `keyring` library) for production deployments.

---

### 7. Encrypt Stored Tokens

**Location:** `auth/gmail_auth.py`

**Enhancement:** Encrypt OAuth tokens at rest using `cryptography.fernet`.

---

### 8. Add Structured Logging

**Issue:** Current logging is basic text format.

**Enhancement:** Consider JSON structured logging for better log aggregation and analysis.

---

## Acceptance Criteria

- [ ] Add type hints to all functions
- [ ] Set up GitHub Actions CI/CD
- [ ] Create CONTRIBUTING.md
- [ ] Create CHANGELOG.md
- [ ] Remove duplicate imports
- [ ] Document secrets management options
- [ ] Document token encryption options
- [ ] Evaluate structured logging

---

**Labels:** `enhancement`, `good-first-issue`, `tech-debt`
