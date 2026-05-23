## Use Specific Exception Types

Never catch generic Exception or Throwable. Catch the most specific exception type possible.

Bad:
catch (Exception e) {
    e.printStackTrace();
}

Good:
catch (SQLException e) {
    logger.error("Database error: {}", e.getMessage());
}

## Use Logger Instead of System.out

Never use System.out.println in production code. Use a proper logging framework like SLF4J or Log4j.

Bad:
System.out.println("Processing user: " + userId);

Good:
logger.info("Processing user: {}", userId);

## Use SecureRandom for Security-Sensitive Code

Never use java.util.Random for security-sensitive operations like token generation.

Bad:
Random random = new Random();
String token = String.valueOf(random.nextInt());

Good:
SecureRandom secureRandom = new SecureRandom();
byte[] token = new byte[32];
secureRandom.nextBytes(token);

## Avoid Hardcoded Credentials

Never hardcode passwords, API keys, or secrets in source code.

Bad:
String password = "admin123";
String apiKey = "sk-abc123";

Good:
String password = System.getenv("DB_PASSWORD");
String apiKey = System.getenv("API_KEY");

## Use Objects.isNull for Null Checks

Prefer Objects.isNull() or Objects.nonNull() over == null for clarity.

Bad:
if (user == null) {
    throw new IllegalArgumentException();
}

Good:
if (Objects.isNull(user)) {
    throw new IllegalArgumentException("User cannot be null");
}

## Close Resources Properly

Always use try-with-resources to ensure resources are closed properly.

Bad:
Connection conn = dataSource.getConnection();
Statement stmt = conn.createStatement();
// connection never closed if exception occurs

Good:
try (Connection conn = dataSource.getConnection();
     Statement stmt = conn.createStatement()) {
    // resources automatically closed
}