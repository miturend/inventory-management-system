from werkzeug.security import generate_password_hash
from database import get_connection


username = "admin"
password = "admin123"

hashed_password = generate_password_hash(password)


connection = get_connection()
cursor = connection.cursor()


cursor.execute("""
INSERT INTO Users
(
    Username,
    PasswordHash,
    Role
)
VALUES
(
    %s,
    %s,
    %s
)
""", (
    username,
    hashed_password,
    "Admin"
))


connection.commit()

cursor.close()
connection.close()


print("Admin user created")