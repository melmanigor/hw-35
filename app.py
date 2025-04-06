from flask import Flask,render_template,request,redirect,url_for,abort
from cart import cart_bp,cart,api_cart_bp
import webbrowser
from threading import Timer

app=Flask(__name__)
app.register_blueprint(cart_bp,url_prefix='/cart')
app.register_blueprint(api_cart_bp,url_prefix='/api')

@app.route('/', methods=['GET','POST'])
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

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__=='__main__':
    Timer(1, open_browser).start()
    app.run(debug=True,use_reloader=False)



