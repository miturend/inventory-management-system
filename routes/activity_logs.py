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
            activitylogs.LogID,
            users.Username,
            activitylogs.Action,
            activitylogs.CreatedDate
        FROM activitylogs
        LEFT JOIN users
            ON activitylogs.UserID = users.UserID
        ORDER BY activitylogs.CreatedDate DESC
    """)

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "activity_logs.html",
        logs=logs
    )