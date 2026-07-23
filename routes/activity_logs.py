from flask import Blueprint, render_template
from database import get_connection
from utils.auth_helpers import admin_required

activity_logs = Blueprint("activity_logs", __name__)


@activity_logs.route("/activity-logs")
@admin_required
def view_activity_logs():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ActivityLogs.LogID,
            Users.Username,
            ActivityLogs.Action,
            ActivityLogs.CreatedDate
        FROM activitylogs
        LEFT JOIN users
            ON ActivityLogs.UserID = Users.UserID
        ORDER BY ActivityLogs.CreatedDate DESC
    """)

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "activity_logs.html",
        logs=logs
    )