import hashlib
import hmac
import json
import os
import urllib.request
from datetime import datetime, timezone

SIGNING_SECRET = os.environ.get("SIGNING_SECRET", "hello-there-from-b12")

GITHUB_SERVER_URL = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "ayushsinghal90/task_b12")
GITHUB_RUN_ID = os.environ.get("GITHUB_RUN_ID", "")

repository_link = f"{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}"
action_run_link = f"{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}"

payload = {
    "action_run_link": action_run_link,
    "email": "ayushsinghal998@gmail.com",
    "name": "Ayush Singhal",
    "repository_link": repository_link,
    "resume_link": "https://www.linkedin.com/in/ayush-singhal-0a994b147/",
    "timestamp": (lambda t: t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z")(datetime.now(timezone.utc)),
}

body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

signature = hmac.new(SIGNING_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()

req = urllib.request.Request(
    "https://b12.io/apply/submission",
    data=body,
    headers={
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}",
    },
    method="POST",
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode("utf-8"))
    print(f"Receipt: {result['receipt']}")
