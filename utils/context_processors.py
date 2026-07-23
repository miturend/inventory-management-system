from database import get_connection

def inject_settings():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Settings
        WHERE SettingID = 1
    """)

    settings = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "system_settings": settings
    }