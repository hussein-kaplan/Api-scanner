# 🔍 API Key Scanner

A Kali-friendly tool to scan for leaked or exposed API keys and identify which service they belong to, using over 1000 known patterns.

- ✅ Supports GitHub, Stripe, Google, AWS, and 1000+ more.
- 🧠 Uses `secrets-patterns-db` and `trufflehog` regex sources.
- 📦 Lightweight, works with Python 3.

---

## 🚀 Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Update pattern database (recommended once)
python3 cli.py update-patterns

# Scan for API keys
python3 cli.py scan keys.txt
```

*You can also use stdin:*
```bash
cat keys.txt | python3 cli.py scan -
```

---

## 🛠️ Example Output:

| API Key                              | Service     | Confidence |
|--------------------------------------|-------------|------------|
| `sk_test_abc123`                     | Stripe      | 0.97       |
| `ghp_abcdEFGHijklMNOP1234567890`     | GitHub      | 0.99       |

---

## 📁 Files

- `cli.py`: The main CLI script
- `requirements.txt`: Python dependencies
- `banner.txt`: ASCII banner (optional)
