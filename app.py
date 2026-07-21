from flask import Flask
from routes.auth import auth
from routes.products import products
from routes.customers import customers
from routes.suppliers import suppliers
from routes.purchases import purchases
from routes.sales import sales
from routes.dashboard import dashboard
app = Flask(__name__)

app.secret_key = "okeysam_inventory_secret"

app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(customers)
app.register_blueprint(suppliers)
app.register_blueprint(purchases)
app.register_blueprint(sales)
app.register_blueprint(dashboard)

if __name__ == "__main__":
    app.run(debug=True)
    