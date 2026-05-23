import re
import json

def extract_json(text: str, default=None):
    if default is None:
        default = []
    # strip markdown fences
    text = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default