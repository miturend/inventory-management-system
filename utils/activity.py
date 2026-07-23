from database import get_connection
from flask import session


def log_activity(action, description):

    connection = get_connection()
    cursor = connection.cursor()

    user_id = session.get("user_id")

    cursor.execute("""
        INSERT INTO activitylogs
        (
            UserID,
            Action,
            Description
        )
        VALUES
        (%s, %s, %s)
    """, (
        user_id,
        action,
        description
    ))

    connection.commit()

    cursor.close()
    connection.close()