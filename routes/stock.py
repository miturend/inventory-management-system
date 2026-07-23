from flask import Blueprint, render_template
from database import get_connection
from utils.auth_helpers import login_required

stock = Blueprint("stock", __name__)


@stock.route("/stock/history")
@login_required
def stock_history():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        stockmovements.MovementID,
        products.ProductName,
        users.Username,
        stockmovements.MovementType,
        stockmovements.Quantity,
        stockmovements.Description,
        stockmovements.CreatedDate
    FROM stockmovements
    INNER JOIN products
        ON stockmovements.ProductID = products.ProductID
    LEFT JOIN users
        ON stockmovements.UserID = users.UserID
    ORDER BY stockmovements.CreatedDate DESC
""")

    movements = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "stock_history.html",
        movements=movements
    )
