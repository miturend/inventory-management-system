import os
import subprocess
from datetime import datetime


MYSQLDUMP_PATH = r"C:\Program Files\MySQL\MySQL Workbench 8.0\mysqldump.exe"
MYSQL_PATH = r"C:\Program Files\MySQL\MySQL Workbench 8.0\mysql.exe"

MYSQL_USER = "root"
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE_NAME = os.getenv("MYSQL_DATABASE")


def create_backup():

    backup_folder = "backups"
    os.makedirs(backup_folder, exist_ok=True)

    filename = datetime.now().strftime(
        "backup_%Y%m%d_%H%M%S.sql"
    )

    filepath = os.path.join(
        backup_folder,
        filename
    )

    command = [
        MYSQLDUMP_PATH,
        "-u",
        MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        DATABASE_NAME
    ]

    with open(filepath, "w") as output:

        result = subprocess.run(
            command,
            stdout=output,
            stderr=subprocess.PIPE,
            text=True
        )

    return result, filename


def restore_database(filename):

    backup_folder = "backups"

    # ---------- Automatic Safety Backup ----------

    safety_name = datetime.now().strftime(
        "AUTO_BACKUP_%Y%m%d_%H%M%S.sql"
    )

    safety_path = os.path.join(
        backup_folder,
        safety_name
    )

    dump_command = [
        MYSQLDUMP_PATH,
        "-u",
        MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        DATABASE_NAME
    ]

    with open(safety_path, "w") as output:

        subprocess.run(
            dump_command,
            stdout=output
        )

    # ---------- Restore Selected Backup ----------

    filepath = os.path.join(
        backup_folder,
        filename
    )

    restore_command = [
        MYSQL_PATH,
        "-u",
        MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        DATABASE_NAME
    ]

    with open(filepath, "r") as backup_file:

        result = subprocess.run(
            restore_command,
            stdin=backup_file,
            stderr=subprocess.PIPE,
            text=True
        )

    return result