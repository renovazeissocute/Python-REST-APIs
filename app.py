from flask import Flask, request, render_template, redirect, jsonify 
import os
import mysql.connector as mysql

conn = mysql.connect(
    host= "localhost",
    user = "root",
    password = "12345678",
    port = 3306,
    database = "my_memo"
)

app = Flask(__name__)
template_folder = os.path.join(os.path.dirname(__file__), "templates/")

app.static_folder = 'static'
app.static_url_path ="/static"

@app.route('/', methods= ['GET']) #API
def index():
    cur = conn.reconnect()

    sql = "SELECT idmemo, firstname, lastname, email FROM memo"
    cur = conn.cursor()
    cur.execute(sql)
    names = cur.fetchall()
    # ('aaa', 'bbb', 'vvv#vvv.com')
    conn.close()
    return render_template("index.html", names=names)

@app.route('/product', methods=["GET"])
def product():
    item = {
        "Name": "Adidas",
        "Model": "Ultra Boots",
        "Price": "180.00"
    }
    return item

@app.route('/news/<id>', methods=["GET"]) #Path parameter
def news(id):
    return "Topic no. is" + id

@app.route('/profile', methods=["GET"]) #Get values from GET method
def profile():
    name = request.args.get("name")
    age = request.args.get("age")
    email = request.args.get("email")
    return "<B>I am "+name+","+age+" years. This is my email:" + email + "</B>"

@app.route('/post-data', methods=["POST"])
def post_data():
    name = request.args.get("name")
    age = request.args.get("age")
    email = request.args.get("email")
    return "<B>I am 555 "+name+","+age+" years. This is my email:" + email + "</B>"

@app.route('/adduser', methods=["GET"])
def add_newuser():
    return render_template('add_user.html')

@app.route('/adduser_todb', methods=["POST"])
def adduser_todb():
    cur = conn.reconnect()

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')

    sql = "INSERT INTO memo(firstname, lastname, email)"
    sql += "VALUES(%s,%s,%s)"
    data = (firstname, lastname, email)

    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<idmemo>', methods=["GET"])
def delete(idmemo):
  
    cur = conn.reconnect()
    sql = "DELETE FROM memo WHERE idmemo=%s"
    data = (idmemo,)
    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<idmemo>', methods=["GET"])
def edit(idmemo):
    cur = conn.reconnect()
    sql ="SELECT idmemo, firstname, lastname, email "
    sql += "FROM memo WHERE idmemo=%s"
    data = (idmemo,)

    cur = conn.cursor()
    cur.execute(sql,data)
    name = cur.fetchone()
    conn.close()

    return render_template("edit_user.html", name=name)

@app.route('/edituser_todb', methods=["POST"])
def edituser_todb():
    cur = conn.reconnect()

    idmemo = request.form.get('idmemo')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')

    sql = "UPDATE memo SET firstname=%s, lastname=%s, email=%s"
    sql += "WHERE idmemo=%s"
    data = (firstname,lastname,email,idmemo)

    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect('/')

# RESTAPIs
@app.route('/getuser', methods=["GET"])
def get_user():
    cur = conn.reconnect()

    sql="SELECT idmemo, firstname, lastname, email "
    sql += " FROM memo ORDER BY firstname"
    cur = conn.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    conn.close()
    return jsonify(records)

@app.route('/postuser', methods=["POST"])
def post_user():
    response = request.get_json()
    firstname = response['firstname']
    lastname = response['lastname']
    email = response['email']

    cur = conn.reconnect()
    cur = conn.cursor()
    sql = "INSERT INTO memo(firstname, lastname, email) "
    sql += "VALUES(%s, %s, %s)"
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return redirect('/getuser/v1/1')

@app.route('/delete/<email>', methods=["DELETE"])
def delete_user(email):
    cur = conn.reconnect()
    cur = conn.cursor()
    sql = "DELETE FROM memo WHERE email=%s " 
    data = (email,)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return redirect('/getuser')

@app.route('/put_user', methods=["PUT"])
def put_user():
    response = request.get_json()
    idmemo = response['idmemo']
    firstname = response['firstname']
    lastname = response['lastname']
    email = response['email']

    #UPDATE DATA TO DB
    cur = conn.reconnect()
    cur = conn.cursor()
    sql = "UPDATE memo SET firstname=%s, lastname=%s, email=%s"
    sql += "WHERE idmemo=%s"
    data = (firstname,lastname,email,idmemo)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return redirect('/getuser')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
