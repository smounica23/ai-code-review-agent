## Naming Conventions

Use snake_case for variables and functions. Use PascalCase for classes.
Avoid single letter variable names except for loop counters.

Bad: def getUsr(): x = db.query()
Good: def get_user(): user = db.query()

## Error Handling

Never use bare except clauses. Always catch specific exceptions.

Bad:
try:
    process()
except:
    pass

Good:
try:
    process()
except ValueError as e:
    logger.error(f"Invalid value: {e}")

## Type Annotations

Always add type annotations to function signatures in Python 3.6+.
This improves readability and enables static analysis tools.

Bad:
def process(data, config):
    return data

Good:
def process(data: dict, config: Config) -> dict:
    return data

## Avoid Mutable Default Arguments

Never use mutable objects as default function arguments. They are shared across calls.

Bad:
def append_item(item, lst=[]):
    lst.append(item)
    return lst

Good:
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

## Use Context Managers for Resources

Always use context managers when working with files, database connections, or network resources.

Bad:
f = open("file.txt")
data = f.read()
f.close()

Good:
with open("file.txt") as f:
    data = f.read()

## Avoid Magic Numbers

Replace magic numbers with named constants.

Bad:
if status == 3:
    send_alert()

Good:
MAX_RETRY_COUNT = 3
if status == MAX_RETRY_COUNT:
    send_alert()

## Use List Comprehensions Appropriately

Prefer list comprehensions over loops for simple transformations but avoid nesting more than 2 levels.

Bad:
result = []
for item in items:
    result.append(item.value)

Good:
result = [item.value for item in items]

## Logging Best Practices

Use the logging module instead of print statements in production code.

Bad:
print(f"Processing user {user_id}")

Good:
logger = logging.getLogger(__name__)
logger.info("Processing user", extra={"user_id": user_id})