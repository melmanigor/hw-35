from flask import Flask,render_template,request,redirect,url_for,abort,flash,send_from_directory,session
from cart import cart_bp,cart,api_cart_bp
import webbrowser
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash
from threading import Timer

app=Flask(__name__)
app.register_blueprint(cart_bp,url_prefix='/cart')
app.register_blueprint(api_cart_bp,url_prefix='/api')
app.secret_key="supersecret123"
UPLOAD_FOLDER= 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg'}

upload_images={}
users = {
    'admin': generate_password_hash("1234"),
    'testuser': generate_password_hash("password")
}
@app.route('/', methods=['GET','POST'])
def index():
    user=session.get('user_id')

    search_query=request.args.get('search','').strip()
    search_results=[]
    if request.method=="POST":
        item=request.form.get('item')
        if item:
            if len(item)>10:
                abort(400)
            if not any(p['name'].lower()==item.lower() for p in cart):
                image_path='images/placeholder.png'
                uploaded=upload_images.get(item)
                if uploaded:
                    if isinstance (uploaded,list):
                        image_path=f"images/{uploaded[0]}"
                    else:
                        image_path=f"images/{uploaded}"
                cart.append({
                  "name":item,
                  "image":image_path  
                })
                return redirect(url_for("cart.show_cart"))
            else:
                return render_template('index.html',message="The item already in cart",search_query=search_query,search_results=search_results)
    if search_query :
        for item in cart:
            if search_query.lower() in item['name'].lower():
                search_results.append(item['name'])
        if not search_results:
                abort(404, description=f"The item '{search_query}' was not found")

    return render_template('index.html',search_query=search_query,search_results=search_results,user=user)
@app.route('/admin/upload',methods=['GET','POST'])
def upload_file():
    if request.method =='POST':
        product_id=request.form.get('product_id')
        file=request.files.get('image')
        if not product_id or not file or file.filename=="":
            flash("Both product id and file name should be enter")
            return redirect(request.url)
        ext=file.filename.rsplit('.')[1].lower()
        unique_name = f"{secure_filename(product_id)}_{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)

        file.save(save_path)
        upload_images[product_id]=unique_name
        flash("Image upload successfully")
        return  redirect(url_for('upload_file')) 
    return render_template('upload.html')
@app.route('/admin/multiple-upload',methods=['GET','POST'])
def upload_multiple_files():
   if request.method=='POST':
       product_id=request.form.get('product_id')
       files=request.files.getlist('images')
       upload_filenames=[]
       for file in files:
           ext=file.filename.rsplit('.',1)[1].lower()
           unique_name=f"{secure_filename(product_id)}_{uuid.uuid4().hex}.{ext}"
           save_path=os.path.join(app.config['UPLOAD_FOLDER'],unique_name)
           file.save(save_path)
           upload_filenames.append(unique_name)
       upload_images[product_id]=upload_filenames
       flash("Multiple images uploaded successfully ")
       return redirect(url_for('upload_multiple_files'))
   return render_template('upload_multiple.html')
@app.route ('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if not username or not password:
            flash("User name or password required")
            return redirect(url_for('signup'))
        if username  in users:
            flash("User name already exist")
            return redirect(url_for('signup'))
        password_hash=generate_password_hash(password)
        users[username]=password_hash
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'] )   
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username not in users:
            flash("User not exist")
            return redirect(url_for('login'))
        if  not check_password_hash(users[username],password):
            flash("Incorrect password or User name")
            return redirect(url_for('login'))
        session['user_id']=username
        flash(f"Welcome {username}!")
        return redirect(url_for('index'))
    return render_template('login.html')
     
@app.route('/admin/images')
def show_upload_images():
    return upload_images
@app.route('/images/<string:image_name>/')
def serve_image(image_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], image_name)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__=='__main__':
    Timer(1, open_browser).start()
    app.run(debug=True,use_reloader=False)



