import os
import requests

# Set up Jira auth and base info
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
auth = (JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def create_issue(summary, description, issue_type, epic_name=None):
    fields = {
        "project": {"key": JIRA_PROJECT_KEY},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type}
    }

    if issue_type == "Story" and epic_name:
        # Set the Epic Link (customfield_10014 must be correct for your Jira instance)
        fields["customfield_10014"] = epic_name

    data = {"fields": fields}
    response = requests.post(
        f"{JIRA_BASE_URL}/rest/api/3/issue",
        json=data,
        headers=headers,
        auth=auth
    )
    if response.status_code == 201:
        print(f"Created {issue_type}: {summary}")
        return response.json()["key"]
    else:
        print(f"Failed to create {issue_type}: {summary}\n{response.text}")
        return None

epics = {
    "User Onboarding & Account Management": [
        "Implement user registration and login functionalities.",
        "Develop user profile management features.",
        "Integrate password recovery and email verification processes."
    ],
    "Voyage Planning & Route Optimization": [
        "Design the voyage input form for users to enter journey details.",
        "Integrate map services for route visualization.",
        "Develop algorithms for optimizing routes based on sustainability metrics."
    ],
    "Emissions Calculation & Reporting": [
        "Implement backend services to calculate emissions based on voyage data.",
        "Create user-friendly dashboards to display emissions reports.",
        "Enable export of emissions data in various formats (PDF, CSV)."
    ],
    "Sustainability Recommendations & Insights": [
        "Develop a recommendation engine for sustainable practices.",
        "Integrate educational content on sustainability into the platform.",
        "Provide real-time alerts and tips during voyage planning."
    ]
}

# Main logic
for epic, stories in epics.items():
    epic_key = create_issue(epic, f"Epic: {epic}", "Epic")
    if epic_key:
        for story in stories:
            create_issue(story, f"Story under {epic}", "Story", epic_key)
