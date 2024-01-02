from flask import Flask, render_template
import psycopg2
from datetime import datetime, timedelta

# PostgreSQL Connection Details
DB_HOST = "rds-db1.cjz9pbxtvmuk.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "rasitha"
DB_PASSWORD = "rasitha123"

# Flask App
app = Flask(__name__)

# Function to fetch GitHub metrics for the last week
def fetch_last_week_github_metrics():
    # Calculate the start date of last week
    last_week_start = datetime.now() - timedelta(days=datetime.now().weekday() + 7)
    
    # Connection to the PostgreSQL database
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Table name to read from
    table_name = "metrics"

    # Query to select data for the last week
    select_query = f"SELECT * FROM {table_name} WHERE created_at >= %s"
    
    try:
        # Execute the query
        cursor.execute(select_query, (last_week_start,))

        # Fetch all rows
        rows = cursor.fetchall()

        # Display the results
        metrics = []
        for row in rows:
            github_metrics.append({
                "username": row[0],
                "commits_count": row[1],
                "open_issues_count": row[2],
                "closed_issue_count": row[3]
                "commit_date": row[4]
            })

        return github_metrics

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Route to display last week's metrics in a browser
@app.route('/')
def display_last_week_metrics():
    last_week_metrics = fetch_last_week_github_metrics()
    date_range = f"Last week's data"
    return render_template('metrics-rds.html', github_metrics=last_week_metrics, date_range=date_range)

if __name__ == '__main__':
    app.run(debug=True)

