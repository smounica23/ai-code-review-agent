## Never Store Plaintext Passwords

Always hash passwords using strong algorithms like bcrypt, scrypt, or Argon2.
Never use MD5 or SHA1 for password hashing — they are cryptographically broken.

Bad:
user.password = plain_password

Good:
user.password = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())

## Use Environment Variables for Secrets

Never hardcode API keys, passwords, database credentials, or tokens in source code.
Always read them from environment variables or a secrets manager.

Bad:
API_KEY = "sk-abc123xyz"
DB_PASSWORD = "supersecret"

Good:
API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")

## Validate All Input

Never trust user input. Always validate type, length, format, and range.

Bad:
def process(user_id):
    return db.query(f"SELECT * FROM users WHERE id={user_id}")

Good:
def process(user_id: int):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user_id")
    return db.query("SELECT * FROM users WHERE id=%s", (user_id,))

## Use HTTPS Everywhere

Never transmit sensitive data over HTTP. Always enforce HTTPS.
Set secure and httpOnly flags on cookies.

## Implement Rate Limiting

Protect all public APIs from brute force and DoS attacks using rate limiting.

Bad:
@app.post("/login")
def login(credentials): ...  # no rate limiting

Good:
@app.post("/login")
@limiter.limit("5/minute")
def login(credentials): ...

## Principle of Least Privilege

Grant only the minimum permissions necessary.
Database users should only have SELECT/INSERT/UPDATE on the tables they need.
Never run application code as root or database admin.

## Dependency Security

Regularly scan dependencies for known vulnerabilities.
Use pip-audit for Python, npm audit for JavaScript, OWASP dependency-check for Java.
Pin all dependency versions in requirements files.

## Sensitive Data in Logs

Never log passwords, tokens, credit card numbers, or personal data.
Mask or redact sensitive fields before logging.

Bad:
logger.info(f"Login attempt: user={username} password={password}")

Good:
logger.info(f"Login attempt: user={username}")