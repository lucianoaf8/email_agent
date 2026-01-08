# High Priority: Critical Security Vulnerabilities & Bugs

## High Priority Issues

These issues require immediate attention due to security risks or critical bugs.

### 1. BUG: Missing `classify_email` Import in main.py

**Location:** `main.py:51`

```python
classification = classify_email(email)  # classify_email not imported!
```

**Current imports:**
```python
from processor import summarize_emails, classify_emails  # Missing: classify_email
```

**Fix:** Add `classify_email` to the import statement.

---

### 2. SECURITY: Insecure Deserialization (Pickle) - CRITICAL

**Location:** `auth/gmail_auth.py:36-37, 84`

**Risk:** Pickle deserialization can execute arbitrary code if the `token.pickle` file is tampered with.

**Fix:** Replace pickle with encrypted JSON storage using the `cryptography` library.

---

### 3. SECURITY: XSS/HTML Injection - HIGH

**Locations:**
- `utils/formatter.py:12-14`
- `sender/send_summary.py:51`

**Risk:** Email subjects and content are embedded in HTML without escaping, allowing script injection.

**Fix:** Use `html.escape()` for all user-controlled content before embedding in HTML.

---

### 4. SECURITY: Prompt Injection - HIGH

**Location:** `processor/summarizer.py:39-43`

**Risk:** Untrusted email content is directly injected into LLM prompts, allowing prompt manipulation.

**Fix:** Sanitize and validate email content before including in prompts.

---

### 5. Missing Dependency in requirements.txt

**Issue:** `python-dotenv` is used throughout the codebase but not listed in `requirements.txt`.

**Fix:** Add `python-dotenv>=1.0.0` to requirements.txt.

---

## Acceptance Criteria

- [ ] Fix missing import bug in main.py
- [ ] Replace pickle with secure token storage
- [ ] Add HTML escaping to all user content in reports
- [ ] Sanitize inputs before LLM prompts
- [ ] Add python-dotenv to requirements.txt

---

**Labels:** `bug`, `security`, `high-priority`
