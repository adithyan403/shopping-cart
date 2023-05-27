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
   

data=[]
db = client['shopping']  # Access the 'mydatabase' database
collection = db['user']
products=collection.find({})
data=products
@app.route('/')
def mainpage():
    count=0
    user_id = session.get('user_id')
    
    try:
        client.admin.command("ping")
    except:
        print("unseccessful cant connect")
    
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['user']
    products=collection.find({})
    data=products
    if user_id:
        collection2=db[user_id]
        count = collection2.count_documents({})
        
    
    return render_template("index.html",items=data,user=user_id,number=count)
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
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/loginbutton",methods=["POST"])
def loginbutton():
    session["status"]=True
    user_id = session.get('user_id')
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
        session["status"]=False
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
    userdata=collection.find({})
    emails=[]
    session["status2"]=False
    for i in userdata:
        emails.append(i["email"])
    if email in emails:
        session["status2"]=True
        return redirect("/sign up")
        
    
   
    else:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        collection.insert_one({"email":email,"password":hashed_password})
        return redirect("/login")
    

@app.route("/cart")
def cart():
    price1=0
    if session.get("user_id"):
        db = client['shopping']  # Access the 'mydatabase' database
        user_id = session.get('user_id')
        collection=db[user_id]
        data=collection.find({})
        usercollections=db[user_id]
        userproducts=usercollections.find({})
        for i in userproducts:
            price1+=int(i["price"])
        

        return render_template("cart.html",items=data,total=price1)
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
product=0
@app.route("/addcart/<item>")
def addcart(item):
    user_id = session.get('user_id')
    
        
    if user_id:
        db = client['shopping']  # Access the 'mydatabase' database
        user_id = session.get('user_id')
        collection=db[user_id]
        collection2=db["user"]
        price=collection2.find_one({"name":item})
    else:
        return redirect("/login")
    

    collection.insert_one({"name":item,"price":price["price"],"image":price["image"]})
    
    return redirect("/")

@app.route("/removecart/<item>")
def removecart(item):
    db = client['shopping']  # Access the 'mydatabase' database
    user_id = session.get('user_id')
    collection=db[user_id]
    collection.delete_one({"name":item})
    return redirect("/cart")
@app.route("/orders")
def order():
    price1=0
    db = client['shopping']  # Access the 'mydatabase' database
    user_id = session.get('user_id')
    collection=db[user_id]
    orders=collection.find({})
    for i in orders:
            price1+=int(i["price"])
    return render_template("order.html",items=orders,total=price1)

@app.route("/continue",methods=["POST"])
def checkout():
    status=False
    price1=0
    db = client['shopping']  # Access the 'mydatabase' database
    user_id = session.get('user_id')
    collection1=db[user_id]
    collection2=db["checkout"]
    home=request.form.get("home")
    city=request.form.get("city")
    state=request.form.get("state")
    code=request.form.get("code")
    payment=request.form.get("payment_method")
    print(payment)
    address=[home,city,state,code]
    orders=list(collection1.find({}))
    items=[]
    for i in orders:
        name=i["name"]
        image=i["image"]
        price=i["price"]
        dic={"name":name,"image":image,"price":price}
        items.append(dic)
    if status==False:
        for i in orders:
            price1+=int(i["price"])
    
    emails=[]
    for i in collection2.find({}):
        emails.append(i["email"])
    if user_id not in emails:
        collection2.insert_one({"email":user_id,"address":address,"orders":orders,"total":price1,"payment":payment})
        print("datainserted")
    if payment=="cash_on_delivery":
        status=True
        collection1.delete_many({})

        return render_template("myorders.html",items=items,total=price1)
    else:
        return render_template("/")
