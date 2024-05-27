from flask import Blueprint, jsonify
from shopify_app.methods import fetch_order_details, fetch_orders, create_mock_shipbob_order

bp = Blueprint('routes', __name__)

@bp.route('/orders', methods=['GET'])
def get_orders():
    orders = fetch_orders()
    print("Orders:")
    for order in orders:
        print(f"Order ID: {order['id']}, Name: {order['name']}")
    return jsonify({"orders": orders})

@bp.route('/order_details/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    order_details = fetch_order_details(order_id)
    if order_details:
        product_names = [item['name'] for item in order_details.get('line_items', [])]
        print(f"Order details for order ID {order_id}:")
        print("Product Names:", product_names)
        return jsonify({"product_names": product_names})
    else:
        return jsonify({"error": f"Failed to fetch order details for order ID {order_id}"}), 500

@bp.route('/mock_shipbob_order/<int:order_id>', methods=['GET'])
def mock_shipbob_order(order_id):
    order_details = fetch_order_details(order_id)
    if order_details:
        shipbob_order = create_mock_shipbob_order(order_details)
        if shipbob_order:
            print("Mock Shipbob Order:")
            print(shipbob_order)
            return jsonify({"shipbob_order": shipbob_order})
        else:
            return jsonify({"error": "Failed to create mock Shipbob order"}), 500
    else:
        return jsonify({"error": f"Failed to fetch order details for order ID {order_id}"}), 500
    
