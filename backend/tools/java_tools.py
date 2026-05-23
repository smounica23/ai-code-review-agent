import re

def run_java_analysis(code: str) -> list[dict]:

    issues = []

    patterns = [
    (r"System\.out\.println\(", "JAVA001", "Use logger instead of System.out.println", "best_practice", "LOW"),
    (r"e\.printStackTrace\(", "JAVA002", "Use logger instead of printStackTrace", "best_practice", "LOW"),
    (r"catch\s*\(\s*Exception\s+\w+\s*\)", "JAVA003", "Too broad exception catch - catch specific exceptions", "best_practice", "MEDIUM"),
    (r"==\s*null", "JAVA004", "Use Objects.isNull() instead of == null", "best_practice", "LOW"),
    (r"new\s+Random\(\)", "JAVA005", "Use SecureRandom instead of Random for security-sensitive code", "security", "MEDIUM"),
    (r"(?i)(password|secret|api_key)\s*=\s*\"[^\"]+\"", "JAVA006", "Possible hardcoded credential found", "security", "HIGH"),
]
    
    for pattern, rule_id, description, category, severity in patterns:
        for match in re.finditer(pattern, code):
            line_number = code[:match.start()].count("\n") + 1
            issues.append({
                "rule_id": rule_id,
                "description": description,
                "line_start": line_number,
                "line_end": line_number,
                "category": category,
                "severity": severity,
                "source": "static_analysis"
            })
    
    return issues