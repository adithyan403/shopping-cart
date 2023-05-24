from flask import Flask,render_template,request
from pymongo import MongoClient as mon

client = mon('mongodb://localhost:27017/')

app=Flask("__name__")

if __name__ == '__name__':
    app.run(debug=True)


data=[]
@app.route('/')
def mainpage():
    try:
        client.admin.command("ping")
        print(" database connected successfull")
    except:
        print("unseccessful cant connect")
    print("server started")
    
    return render_template("index.html",items=data)
@app.route('/admin')
def adminpage():
    
    return render_template('admin.html')
@app.route('/viewproducts')
def view():
   
    return render_template("view products.html",items=data)

@app.route("/add products")
def add():
    return render_template("add product.html")

@app.route("/submit",methods=['POST'])
def submit1():
    name=request.form.get("name")
    price=request.form.get("price")
    category=request.form.get("category")
    image=request.files['image']
    dataimage=image.read()
    db = client['shopping']  # Access the 'mydatabase' database
    collection = db['user']
    collection.insert_one({"name":name,"price":price,"category":category,"image":dataimage})
    print("data inserted successfully")
    products=collection.find_one()
    data.append(products)
    return render_template("view products.html",items=data)
