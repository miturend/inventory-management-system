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
            StockMovements.MovementID,
            Products.ProductName,
            Users.Username,
            StockMovements.MovementType,
            StockMovements.Quantity,
            StockMovements.Description,
            StockMovements.CreatedDate
        FROM StockMovements
        INNER JOIN Products
            ON StockMovements.ProductID = Products.ProductID
        LEFT JOIN Users
            ON StockMovements.UserID = Users.UserID
        ORDER BY StockMovements.CreatedDate DESC
    """)

    movements = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "stock_history.html",
        movements=movements
    )