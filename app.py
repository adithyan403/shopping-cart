from flask import Flask,render_template,request,session,redirect
from pymongo import MongoClient as mon
import bcrypt
from flask_session import Session


client = mon('mongodb://localhost:27017/')

app=Flask("__name__")
app.config['SECRET_KEY'] = 'key'  # Replace with a secure secret key
app.secret_key = app.config['SECRET_KEY']

if __name__ == '__name__':
    app.run(debug=True)
   
price=0
data=[]
db = client['shopping']  # Access the 'mydatabase' database
collection = db['user']
products=collection.find({})
data=products
@app.route('/')
def mainpage():
    user_id = session.get('user_id')
    
    try:
        client.admin.command("ping")
    except:
        print("unseccessful cant connect")
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['user']
    products=collection.find({})
    data=products
    print(data)
    return render_template("index.html",items=data,user=user_id)
@app.route('/admin')
def adminpage():
    
    return render_template('admin.html',items=data)
@app.route('/viewproducts')
def view():
    user_id = session.get('user_id')
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['user']
    products=collection.find({})
    data=products
    
   
    return render_template("view products.html",items=data)

@app.route("/add products")
def add():
    return render_template("add product.html")

@app.route("/submit",methods=['POST'])
def submit1():
    name=request.form.get("name")
    price=request.form.get("price")
    category=request.form.get("category")
    image=request.form.get('image')
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['user']
    collection.insert_one({"name":name,"price":price,"category":category,"image":image})
    print("data inserted successfully")
    products=collection.find({})
    data=products
    return redirect("/viewproducts")


@app.route("/login")
def login():
    return render_template("login.html",status=login)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/loginbutton",methods=["POST"])
def loginbutton():
    email=request.form.get("email")
    password=request.form.get("password")
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['data']
    userdata=collection.find({})
    
    for i in userdata:
        password_data=i["password"]
        entered_password_hash = bcrypt.hashpw(password.encode('utf-8'), password_data)
        if i["email"]==email  and password_data==entered_password_hash:
            session['user_id'] = email
            session['password']=password
            
            
            return redirect("/")
        else:
            continue
    else:
        return redirect("/login")
        
    

@app.route("/sign up")
def signup():
    return render_template("signup.html")
@app.route("/signbutton",methods=["POST"])
def signupbutton():
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['data']
    email=request.form.get("email")
    password=request.form.get("password")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    collection.insert_one({"email":email,"password":hashed_password})
    return redirect("/login")

@app.route("/cart")
def cart():
    if session.get("user_id"):
        db = client['shopping']  # Access the 'mydatabase' database
        user_id = session.get('user_id')
        collection=db[user_id]
        data=collection.find({})

        return render_template("cart.html",items=data)
    else:
        return redirect("/login")
    
@app.route("/delete",methods=["POST"])
def delete():
    id=request.form.get("name")
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['user']
    result = collection.delete_one({'name': id})

    if result.deleted_count > 0:
        return redirect("/viewproducts")
    else:
        return f"No item found with given ID"
    
@app.route("/deletepage")
def deletepage():
    return render_template("delete.html")

@app.route("/editproduct")
def edit():
    return render_template("edit.html")
@app.route("/editsubmit",methods=["POST"])
def editsubmit():
    name=request.form.get("name")
    price=request.form.get("price")
    category=request.form.get("category")
    image=request.form.get('image')
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['user']
    collection.update_one({"name":name},{'$set': {"name":name,"price":price,"category":category,"image":image}})
    return redirect("/viewproducts") 

@app.route("/addcart/<item>")
def addcart(item):
    db = client['shopping']  # Access the 'mydatabase' database
    user_id = session.get('user_id')
    collection=db[user_id]
    collection2=db["user"]
    price=collection2.find_one({"name":item})

    collection.insert_one({"name":item,"price":price["price"]})
    
    return redirect("/")

