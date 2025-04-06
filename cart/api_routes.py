from flask import Blueprint, Flask,render_template,request,redirect,url_for,abort,jsonify
from .cart_routes import cart
api_cart_bp=Blueprint('api_cart',__name__)


@api_cart_bp.route('/items',methods=['GET'])
def get_items():
    return jsonify(cart)

@api_cart_bp.route('/items',methods=['POST'])
def add_item():
    data=request.get_json()
    
    item=data.get('item')
    
    if not item:
        return jsonify({"error": "Missing item field"}),400
    
    if item in cart:
        return jsonify({"error":"Item already in cart"}),400
    cart.append(item)
    return jsonify({"message":f"Item '{'item'}' added"}),201

@api_cart_bp.route('/items/<path:item>',methods=["DELETE"])
def remove_item(item):
    if item in cart:
        cart.remove(item)
        return jsonify ({"message":"removed"}),200
    return jsonify({"message":"not found"}),404

@api_cart_bp.app_errorhandler(404)
def route_not_found(error):
    return jsonify({"error":"Api route not found"}),404
@api_cart_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({"error":"Bad request"}),400
@api_cart_bp.app_errorhandler(500)
def api_500(error):
    return jsonify({"error": "Internal server error"}), 500