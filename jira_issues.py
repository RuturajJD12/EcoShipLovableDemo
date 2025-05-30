import os
import requests

# Load from GitHub Secrets
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

auth = (JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def create_issue(summary, description, issue_type="Task"):
    data = {
        "fields": {
            "project": { "key": JIRA_PROJECT_KEY },
            "summary": summary,
            "description": description,
            "issuetype": { "name": issue_type }
        }
    }

    response = requests.post(
        f"{JIRA_BASE_URL}/rest/api/3/issue",
        json=data,
        headers=headers,
        auth=auth
    )

    if response.status_code == 201:
        key = response.json()["key"]
        print(f"✅ Created {issue_type}: {summary} ({key})")
        return key
    else:
        print(f"❌ Failed to create {issue_type}: {summary}")
        print(response.text)
        return None

# ---- Define Kanban Tasks ---- #
kanban_tasks = [
    "Set up user authentication flow (login/signup)",
    "Build user profile page with editable fields",
    "Implement voyage input form (origin, destination, vessel type)",
    "Integrate map view to display route",
    "Connect emissions calculation backend to voyage form",
    "Display emissions summary and sustainability score",
    "Design dashboard with voyage history",
    "Add sustainability recommendation engine (tips section)",
    "Enable download/export of emissions report (PDF/CSV)",
    "Integrate feedback loop on recommendations"
]

# ---- Create tasks ---- #
for task in kanban_tasks:
    create_issue(task, f"Task: {task}")
