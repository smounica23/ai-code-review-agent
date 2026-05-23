## A1 - Injection

Injection flaws occur when untrusted data is sent to an interpreter as part of a command or query.
The most common type is SQL injection where user input is directly concatenated into a SQL query.

Vulnerable pattern:
query = "SELECT * FROM users WHERE id = " + user_id

Fix: Always use parameterized queries or prepared statements.
query = "SELECT * FROM users WHERE id = %s", (user_id,)

Related rule: CWE-89, Bandit rule B608.

## A2 - Broken Authentication

Weak authentication allows attackers to compromise passwords, keys, or session tokens.
Common issues include hardcoded credentials, weak passwords, and missing session expiration.

Vulnerable pattern:
password = "admin123"
if user_input == password:

Fix: Never hardcode credentials. Use environment variables and strong hashing like bcrypt.
Related rule: CWE-259, Bandit rule B105.

## A3 - Sensitive Data Exposure

Applications expose sensitive data like passwords, credit card numbers, or health records without proper protection.
Common causes include storing data in plain text or transmitting over unencrypted channels.

Vulnerable pattern:
logging.info(f"User password: {password}")

Fix: Never log sensitive data. Encrypt sensitive fields at rest. Use HTTPS for all transmission.
Related rule: CWE-312.

## A4 - XML External Entities (XXE)

XXE attacks target applications that parse XML input. Attackers can use XXE to read files, perform SSRF, or execute remote code.

Vulnerable pattern:
parser = etree.XMLParser(resolve_entities=True)

Fix: Disable external entity processing in all XML parsers.
parser = etree.XMLParser(resolve_entities=False)

Related rule: CWE-611.

## A5 - Broken Access Control

Access control enforces policy such that users cannot act outside of their intended permissions.
Common issues include missing authorization checks and insecure direct object references.

Vulnerable pattern:
def get_user(user_id):
    return db.query(User).filter_by(id=user_id).first()
# No check if current user has permission to access this user_id

Fix: Always verify that the current user has permission to access the requested resource.
Related rule: CWE-284.

## A6 - Security Misconfiguration

Security misconfiguration is the most common issue. It includes default credentials, open cloud storage, verbose error messages, and unnecessary features enabled.

Vulnerable pattern:
DEBUG = True  # left enabled in production
app.run(debug=True)

Fix: Disable debug mode in production. Use environment-specific configuration.
Related rule: CWE-16.

## A7 - Cross-Site Scripting (XSS)

XSS flaws occur when an application includes untrusted data in a web page without proper validation or escaping.
Attackers can execute scripts in the victim's browser.

Vulnerable pattern:
return f"<h1>Hello {user_input}</h1>"  # unescaped user input in HTML

Fix: Always escape user input before rendering in HTML. Use templating engines that auto-escape.
Related rule: CWE-79.

## A8 - Insecure Deserialization

Insecure deserialization allows attackers to execute arbitrary code by passing malicious serialized objects.

Vulnerable pattern:
import pickle
data = pickle.loads(user_input)

Fix: Never deserialize data from untrusted sources using pickle. Use JSON instead.
Related rule: CWE-502, Bandit rule B301.

## A9 - Using Components with Known Vulnerabilities

Using outdated libraries with known vulnerabilities puts the entire application at risk.

Fix: Regularly audit dependencies using tools like pip-audit or safety.
Pin dependency versions in requirements.txt.
Run dependency checks in CI/CD pipeline.
Related rule: CWE-1104.

## A10 - Insufficient Logging and Monitoring

Without proper logging, attacks go undetected. Applications should log authentication failures, access control failures, and input validation failures.

Vulnerable pattern:
except Exception:
    pass  # silently swallowing errors

Fix: Always log exceptions with context. Set up alerts for suspicious patterns.
Use structured logging with correlation IDs.
Related rule: CWE-778.