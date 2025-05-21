import json
from pathlib import Path

def load_findings():
    vulns = Path("reports/vulnerabilities.txt").read_text(errors="ignore")
    leaks = Path("reports/github_leaks.json").read_text(errors="ignore")
    dmarc = Path("reports/dmarc_check.txt").read_text(errors="ignore")
    ssl = Path("reports/sslcheck.txt").read_text(errors="ignore")

    return {
        'vulns': len(vulns.splitlines()),
        'leaks': len([x for x in leaks.splitlines() if "findings" in x]),
        'has_dmarc': "DMARC1" in dmarc,
        'weak_ssl': "TLSv1.0" in ssl or "TLSv1.1" in ssl,
    }

def calculate_score(findings):
    score = 100

    if findings['vulns'] > 0:
        score -= 10 * min(findings['vulns'], 5)

    if findings['leaks'] > 0:
        score -= 20

    if not findings['has_dmarc']:
        score -= 10

    if findings['weak_ssl']:
        score -= 10

    return max(score, 0)

def save_result(score, findings):
    result = {
        "score": score,
        "timestamp": "NOW",
        "details": findings
    }
    with open("reports/latest.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    findings = load_findings()
    score = calculate_score(findings)
    save_result(score, findings)
    print(f"[+] Score calculado: {score}/100")
