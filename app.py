from flask import Flask
from routes.auth import auth
from routes.products import products
from routes.customers import customers
from routes.suppliers import suppliers
from routes.purchases import purchases
from routes.sales import sales
from routes.dashboard import dashboard
from routes.reports import reports
from routes.expenses import expenses
from routes.users import users
from routes.activity_logs import activity_logs
from routes.backup import backup
from routes.stock import stock
from routes.adjustments import adjustments
from routes.receipts import receipts
from routes.settings import settings

app = Flask(__name__)

app.secret_key = "okeysam_inventory_secret"
@app.context_processor
def inject_settings():
    from database import get_connection

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM settings
        WHERE SettingID = 1
    """)

    settings = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "system_settings": settings
    }

app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(customers)
app.register_blueprint(suppliers)
app.register_blueprint(purchases)
app.register_blueprint(sales)
app.register_blueprint(dashboard)
app.register_blueprint(reports)
app.register_blueprint(expenses)
app.register_blueprint(users)
app.register_blueprint(activity_logs)
app.register_blueprint(backup)
app.register_blueprint(stock)
app.register_blueprint(adjustments)
app.register_blueprint(receipts)
app.register_blueprint(settings)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)