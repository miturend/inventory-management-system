from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from utils.auth_helpers import admin_required
from utils.activity import log_activity
import os

from utils.backup import (
    create_backup,
    restore_database
)

backup = Blueprint("backup", __name__)




@backup.route("/backup")
@admin_required
def view_backup():

    backup_folder = "backups"

    os.makedirs(backup_folder, exist_ok=True)

    backup_files = sorted(
        os.listdir(backup_folder),
        reverse=True
    )

    return render_template(
        "backup.html",
        backups=backup_files
    )


@backup.route("/backup/create")
@admin_required
def create_backup_route():

    result, filename = create_backup()

    if result.returncode != 0:

        flash(result.stderr, "danger")

        return redirect(url_for("backup.view_backup"))

    log_activity(
        "DATABASE BACKUP",
        f"Created backup: {filename}"
    )

    flash(
        "Database backup created successfully.",
        "success"
    )

    return redirect(url_for("backup.view_backup"))

from flask import send_from_directory

@backup.route("/backup/download/<filename>")
@admin_required
def download_backup(filename):

    return send_from_directory(
        "backups",
        filename,
        as_attachment=True
    )

@backup.route("/backup/delete/<filename>")
@admin_required
def delete_backup(filename):

    filepath = os.path.join(
        "backups",
        filename
    )

    if os.path.exists(filepath):

        os.remove(filepath)

        log_activity(
            "DELETE BACKUP",
            f"Deleted backup: {filename}"
        )

        flash(
            "Backup deleted successfully.",
            "success"
        )

    return redirect(
        url_for("backup.view_backup")
    )    
@backup.route("/backup/restore/<filename>", methods=["GET", "POST"])
@admin_required
def restore_backup(filename):

    if request.method == "GET":
        return render_template(
            "restore_backup.html",
            filename=filename
        )

    confirmation = request.form["confirm"]

    if confirmation != "RESTORE":

        flash(
            "You must type RESTORE to continue.",
            "danger"
        )

        return redirect(
            url_for(
                "backup.restore_backup",
                filename=filename
            )
        )

    result = restore_database(filename)

    if result.returncode != 0:

        flash(result.stderr, "danger")

        return redirect(
            url_for("backup.view_backup")
        )

    log_activity(
        "RESTORE DATABASE",
        f"Restored backup: {filename}"
    )

    flash(
        "Database restored successfully.",
        "success"
    )

    return redirect(
        url_for("backup.view_backup")
    )