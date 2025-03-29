from flask import Flask,render_template,request,redirect,url_for
import webbrowser
from threading import Timer

app=Flask(__name__)

cart=[]


@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="POST":
        item=request.form.get('item')
        if item:
            if item not in cart:
                cart.append(item)
                return redirect(url_for("show_cart"))
            else:
                return render_template('index.html',message="The item already in cart")
    return render_template('index.html')


@app.route('/cart/')
def show_cart():
    return render_template("cart.html",cart=cart)

@app.route('/remove_item/<path:item>',methods=["DELETE"])
def remove_item(item):
    if item in cart:
        cart.remove(item)
        return "removed",200
    return "not found",404
    

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__=='__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)



