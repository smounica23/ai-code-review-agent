import re
import json

import re
import json

def extract_json(text: str, default=None):
    if default is None:
        default = []
    text = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            fixed = re.sub(r'(?<!\\)\n(?=[^"]*"(?:[^"\\]|\\.)*")', r'\\n', text)
            return json.loads(fixed)
        except json.JSONDecodeError:
            return default