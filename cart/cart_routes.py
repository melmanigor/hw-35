from flask import Blueprint, Flask,render_template,request,redirect,url_for,abort


cart_bp=Blueprint('cart',__name__,template_folder='templates')
cart=[]


@cart_bp.route('/', methods=['GET','POST'])
def index():
    search_query=request.args.get('search','').strip()
    search_results=[]
    if request.method=="POST":
        item=request.form.get('item')
        if item:
            if len(item)>10:
                abort(400)
            if item not in cart:
                cart.append(item)
                return redirect(url_for("cart.show_cart"))
            else:
                return render_template('index.html',message="The item already in cart",search_query=search_query,search_results=search_results)
    if search_query :
        for item in cart:
            if search_query.lower() in item.lower():
                search_results.append(item)
            if not search_results:
                abort(404, description=f"The item '{search_query}' was not found")

    return render_template('index.html',search_query=search_query,search_results=search_results)

@cart_bp.route('/view_cart')
def show_cart():
    return render_template("cart.html",cart=cart)

@cart_bp.route('/remove_item/<path:item>',methods=["DELETE"])
def remove_item(item):
    if item in cart:
        cart.remove(item)
        return "removed",200
    return "not found",404

@cart_bp.app_errorhandler(404)
def item_not_found(error):
    return render_template("404.html",error=error),404

@cart_bp.app_errorhandler(400)
def item_not_found(error):
    return render_template("400.html",error=error),404

