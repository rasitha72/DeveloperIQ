import requests
import psycopg2
from datetime import datetime, timedelta
from flask import Flask, render_template

# GitHub API Token (generate one in your GitHub account settings)
GITHUB_TOKEN = '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'

# PostgreSQL Connection Details
DB_HOST = "rds-db1.cjz9pbxtvmuk.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "rasitha"
DB_PASSWORD = "rasitha123"

# Contributors(GitHub usernames)
contributors = ['rasitha72', 'ekmett', 'Raynos', 'postmodern', 'isaacs']

# Function to make API requests to GitHub GraphQL API
def github_graphql_request(query, variables=None):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v4.idl"
    }
    data = {"query": query, "variables": variables}
    response = requests.post("https://api.github.com/graphql", json=data, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to fetch GitHub metrics
def fetch_github_metrics():
    github_metrics = []
    for contributor in contributors:
        variables = {"login": contributor, "since": yesterday_str}
        response_data = github_graphql_request(graphql_query, variables)
        metrics_data = response_data.get("data", {}).get("user", {}).get("contributionsCollection", {})
        github_metrics.append({
            "username": contributor,
            "metric_type": "commit",
            "metric_data": metrics_data.get("totalCommitContributions", 0)
        })
        github_metrics.append({
            "username": contributor,
            "metric_type": "issue",
            "metric_data": metrics_data.get("totalIssueContributions", 0)
        })
        github_metrics.append({
            "username": contributor,
            "metric_type": "pull_request",
            "metric_data": metrics_data.get("totalPullRequestContributions", 0)
        })
        github_metrics.append({
            "username": contributor,
            "metric_type": "open_issue",  # Modified this line
            "metric_data": metrics_data.get("totalIssueContributions", 0)  # Use totalIssueContributions for open issues
        })
    return github_metrics

# Flask App
app = Flask(__name__)

# Get yesterday's date
yesterday = datetime.now() - timedelta(days=7)
yesterday_str = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")

# GraphQL Query
graphql_query = """
    query GetMetrics($login: String!, $since: DateTime!) {
        user(login: $login) {
            login
            contributionsCollection(from: $since) {
                totalCommitContributions
                totalIssueContributions
                totalPullRequestContributions
            }
        }
    }
"""

# Route to display metrics in a browser
@app.route('/')
def display_metrics():
    github_metrics = fetch_github_metrics()
    date_range = f"{yesterday_str} to {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}"
    return render_template('metrics.html', github_metrics=github_metrics, date_range=date_range)

if __name__ == '__main__':
    app.run(debug=True)

