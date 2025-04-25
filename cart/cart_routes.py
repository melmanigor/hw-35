from flask import Blueprint, render_template, request, redirect, url_for, abort,session

cart_bp = Blueprint('cart', __name__, template_folder='templates')
cart = session.get('cart',[])
@cart_bp.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search', '').strip()
    search_results = []

    if request.method == "POST":
        item = request.form.get('item')
        if item:
            if len(item) > 10:
                abort(400)

        
            if not any(p['name'].lower() == item.lower() for p in cart):
                image_path = 'images/placeholder.png' 
                cart.append({
                    "name": item,
                    "image": image_path
                })
                return redirect(url_for("cart.show_cart"))
            else:
                return render_template(
                    'index.html',
                    message="The item already in cart",
                    search_query=search_query,
                    search_results=search_results
                )

   
    if search_query:
        for item in cart:
            if search_query.lower() in item['name'].lower():
                search_results.append(item['name'])
        if not search_results:
            abort(404, description=f"The item '{search_query}' was not found")

    return render_template('index.html', search_query=search_query, search_results=search_results)

@cart_bp.route('/view_cart')
def show_cart():
    return render_template("cart.html", cart=cart)

@cart_bp.route('/remove_item/<path:item>', methods=["DELETE"])
def remove_item(item):
    for i in cart:
        if i['name'] == item:
            cart.remove(i)
            return "removed", 200
    return "not found", 404


@cart_bp.app_errorhandler(404)
def item_not_found(error):
    return render_template("404.html", error=error), 404

@cart_bp.app_errorhandler(400)
def item_bad_request(error):
    return render_template("400.html", error=error), 400
