from flask import Blueprint, request, jsonify, session

api_cart_bp = Blueprint('api_cart', __name__)

@api_cart_bp.route('/items', methods=['GET'])
def get_items():
    cart = session.get('cart', [])
    return jsonify(cart)

@api_cart_bp.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    item = data.get('item')

    if not item:
        return jsonify({"error": "Missing item field"}), 400

    cart = session.get('cart', [])

    if any(existing_item['name'].lower() == item.lower() for existing_item in cart):
        return jsonify({"error": "Item already in cart"}), 400

    
    cart.append({
        "name": item,
        "quantity": 1,
        "image": "images/placeholder.png"
    })
    session['cart'] = cart
    session.modified = True

    return jsonify({"message": f"Item '{item}' added"}), 201

@api_cart_bp.route('/items/<path:item>', methods=["DELETE"])
def remove_item(item):
    cart = session.get('cart', [])
    updated_cart = []
    found = False

    for product in cart:
        if product['name'].lower() != item.lower():
            updated_cart.append(product)
        else:
            found = True

    if found:
        session['cart'] = updated_cart
        session.modified = True
        return jsonify({"message": "Item removed"}), 200
    else:
        return jsonify({"message": "Item not found"}), 404


@api_cart_bp.app_errorhandler(404)
def route_not_found(error):
    return jsonify({"error": "API route not found"}), 404

@api_cart_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@api_cart_bp.app_errorhandler(500)
def api_500(error):
    return jsonify({"error": "Internal server error"}), 500
