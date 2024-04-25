from models import db, Sweet, Vendor, VendorSweet
from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os
from models import db, Vendor, Sweet, VendorSweet

app = Flask(__name__, template_folder='templates', static_folder='templates')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Migrate with app and db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
# Routes
@app.route('/vendors')
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify([serialize_vendor(vendor) for vendor in vendors])

migrate = Migrate(app, db)
@app.route('/vendors/<int:id>')
def get_vendor(id):
    vendor = Vendor.query.get(id)
    if vendor:
        return jsonify({
            "id": vendor.id,
            "name": vendor.name,
            "vendor_sweets": [serialize_vendor_sweet(vs) for vs in vendor.vendor_sweets]
        })
    return jsonify({"error": "Vendor not found"}), 404

db.init_app(app)
@app.route('/sweets')
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([serialize_sweet(sweet) for sweet in sweets])

@app.route('/sweets/<int:id>')
def get_sweet(id):
    sweet = Sweet.query.get(id)
    if sweet:
        return jsonify(serialize_sweet(sweet))
    return jsonify({"error": "Sweet not found"}), 404

@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.json
    price = data.get('price')
    vendor_id = data.get('vendor_id')
    sweet_id = data.get('sweet_id')

    if None in [price, vendor_id, sweet_id]:
        return jsonify({"errors": ["Missing required fields"]}), 400

    try:
        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative")
    except ValueError:
        return jsonify({"errors": ["Invalid price value"]}), 400

    vendor = Vendor.query.get(vendor_id)
    sweet = Sweet.query.get(sweet_id)

    if vendor is None or sweet is None:
        return jsonify({"errors": ["Vendor or Sweet not found"]}), 404

    vendor_sweet = VendorSweet(price=price, vendor=vendor, sweet=sweet)
    db.session.add(vendor_sweet)
    db.session.commit()

    return jsonify(serialize_vendor_sweet(vendor_sweet)), 201

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = VendorSweet.query.get(id)
    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({}), 204
    return jsonify({"error": "VendorSweet not found"}), 404

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'
def index():
    vendors = Vendor.query.all()
    return render_template('index.html', vendors=vendors)

# Set serialization rules
def serialize_vendor(vendor):
    return {
        "id": vendor.id,
        "name": vendor.name
    }

def serialize_vendor_sweet(vendor_sweet):
    return {
        "id": vendor_sweet.id,
        "price": vendor_sweet.price,
        "sweet": serialize_sweet(vendor_sweet.sweet),
        "sweet_id": vendor_sweet.sweet_id,
        "vendor": serialize_vendor(vendor_sweet.vendor),
        "vendor_id": vendor_sweet.vendor_id
    }

def serialize_sweet(sweet):
    return {
        "id": sweet.id,
        "name": sweet.name
    }

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    app.run(debug=True, port=5000)