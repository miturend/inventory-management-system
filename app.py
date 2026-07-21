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
app = Flask(__name__)

app.secret_key = "okeysam_inventory_secret"

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

if __name__ == "__main__":
    app.run(debug=True)
    