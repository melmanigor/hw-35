from flask import Blueprint, render_template, request, redirect, url_for, abort,session

cart_bp = Blueprint('cart', __name__, template_folder='templates')
@cart_bp.route('/', methods=['GET', 'POST'])
def index():
    cart = session.get('cart',[])

    search_query = request.args.get('search', '').strip()
    search_results = []

    if request.method == "POST":
        item = request.form.get('item')
        quantity=request.form.get('quantity',1,type=int)
        if item:
            if len(item) > 10:
                abort(400)

        
            if not any(p['name'].lower() == item.lower() for p in cart):
                image_path = 'images/placeholder.png' 
                cart.append({
                    "name": item,
                    "quantity":quantity,
                    "image": image_path
                })
                session['cart']=cart
                session.modified=True
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
    cart=session.get('cart',[])
    return render_template("cart.html", cart=cart)

@cart_bp.route('/remove_item/<path:item>', methods=["POST"])
def remove_item(item):
    cart=session.get('cart',[])
    updated_cart = []
    found=False

    for i in cart:
        if i['name'] != item:
            updated_cart.append(i)
        else:
            found=True
    if found:
        session['cart']=updated_cart
        session.modified=True
        return "removed",200
    else:
        return "not found", 404
@cart_bp.route('/update_quantity', methods=['POST'])
def update_quantity():
    item_name = request.form.get('item')
    delta = int(request.form.get('delta', 0))

    cart = session.get('cart', [])
    for product in cart:
        if product['name'].lower() == item_name.lower():
            product['quantity'] += delta
            if product['quantity'] <= 0:
                cart.remove(product)
            session['cart'] = cart
            session.modified = True
            return redirect(url_for('cart.show_cart'))

    return redirect(url_for('cart.show_cart'))



@cart_bp.app_errorhandler(404)
def item_not_found(error):
    return render_template("404.html", error=error), 404

@cart_bp.app_errorhandler(400)
def item_bad_request(error):
    return render_template("400.html", error=error), 400
