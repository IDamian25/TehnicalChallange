from config import SHOP_URL, ACCESS_TOKEN
import requests


def get_headers():
    return {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }

def fetch_orders():
    url = f"{SHOP_URL}/orders.json?status=any"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json().get('orders', [])
    else:
        print(f"Failed to fetch orders: {response.status_code}")
        return []

def fetch_order_details(order_id):
    url = f"{SHOP_URL}/orders/{order_id}.json"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json().get('order', {})
    else:
        print(f"Failed to fetch order details for order ID {order_id}: {response.status_code}")
        return None

def create_mock_shipbob_order(order):
    if not order:
        return None
    
    shipbob_order = {
        "order_id": order['id'],
        "recipient": {
            "first_name": order['shipping_address']['first_name'],
            "last_name": order['shipping_address']['last_name'],
            "address_line1": order['shipping_address']['address1'],
            "city": order['shipping_address']['city'],
            "state": order['shipping_address']['province'],
            "postal_code": order['shipping_address']['zip'],
            "country_code": order['shipping_address']['country_code'],
            "phone_number": order['shipping_address']['phone']
        },
        "items": [{"product_id": "123456", "quantity": item['quantity']} for item in order.get('line_items', [])]
    }
    return shipbob_order
