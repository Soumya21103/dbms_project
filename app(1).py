from flask import Flask, jsonify,render_template,request, redirect, url_for, session
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import time    
import random
app=Flask(__name__)

app.secret_key = "falana"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='mint'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='richflex'

mysql=MySQL(app)
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    print(request)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        c_id=request.form['email']
        password = request.form['password']
        print(c_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer where email = % s and password = % s', (c_id, password, ))
        account = cursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            session['c_id'] = account['C_ID']
            session['First_Name'] = account['First_Name']
            msg = 'Logged in successfully !'
            print(msg)
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
            print(msg)
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('First_Name', None)
   return redirect(url_for('login'))
 
@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    msg = ''
    print(request)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        c_id=request.form['username']
        password = request.form['password']
        print(c_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Admin where username = % s and password = % s', (c_id, password, ))
        account = cursor.fetchone()
        print(account)
        if account:
            session['adminloggedin'] = True
            session['a_id'] = account['Admin_ID']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            print(msg)
            return render_template('admin.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
            print(msg)
    return render_template('admin_login.html', msg = msg)
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'First_Name' in request.form and 'Last_name' in request.form and 'email' in request.form and 'DOB' in request.form and 'Age' in request.form and 'gender' in request.form and 'Membership' in request.form and 'password' in request.form:
        c_id=request.form['email']
        First_Name = request.form['First_Name']
        Last_name = request.form['Last_name']
        email = request.form['email']
        DOB = request.form['DOB'] 
        Age = request.form['Age']
        gender = request.form['gender']
        Membership = request.form['Membership']
        password = request.form['password']   
        Admin_ID = 1
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer where email = % s and First_Name= % s and password = % s', (c_id,First_Name, password, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', First_Name):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO customer VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (c_id,First_Name, Last_name, email, DOB, Age, gender, Membership, password, Admin_ID, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route("/home")
def index():
    if 'loggedin' in session:
        return render_template("home.html")
    return redirect(url_for('login.html'))

@app.route("/product/<id>")
def product(id):
    if 'loggedin' in session:
        return render_template("product.html",id=id)
    return redirect(url_for('login.html'))

@app.route("/addtocart/<id>", methods =['GET', 'POST'])
def atc(id):
    if 'loggedin' in session:
        if request.method == 'POST' and 'quantity' in request.form:
            quantity = request.form['quantity']
            cnx=mysql.connection.cursor()
            cnx.execute("INSERT INTO cart (C_ID, P_ID, Quantity) VALUES (%s, %s, %s);",(session['c_id'],id,quantity,))
            mysql.connection.commit()
            print(cnx.fetchall())
            return redirect("/home")
    return redirect(url_for('login.html'))

@app.route("/purchase")#todo
def purchase():
    if 'loggedin' in session:
        return render_template("product.html",id=id)
    return redirect(url_for('login.html'))

@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE c_id = % s', (session['c_id'], ))
        account = cursor.fetchone()   
        return render_template("home.html", account = account)
    return redirect(url_for('login.html'))
@app.route("/catdata")
def get_data():
    cnx=mysql.connection.cursor()
    cnx.execute("Select * from Category")
    data=[{'id':i[0],'name':i[1]} for i in cnx.fetchall()]
    cnx.close()
    print(data)
    return jsonify(data)

@app.route("/productdata/<id>" ,methods =['GET', 'POST'])
def get_data1(id):
    msg = ''
    cursor = mysql.connection.cursor()
    cursor.execute('select NP_id, Pname, quantity, price from N_Product n,Category c where n.cat_id=c.cat_id and c.cat_id=% s',(id, ))
    data=[{'id':i[0],'name':i[1],'category':i[2],'price':i[3]} for i in cursor.fetchall()]
    return render_template('result.html',data =json.dumps(data))
 
    
@app.route("/cartdata1")
def get_data2():
    cnx=mysql.connection.cursor()
    cnx.execute("select c.C_ID, p.nP_ID, p.PName, p.Price, c.Quantity, (p.Price * c.Quantity) AS Total_Price FROM cart c,N_Product p where c.P_ID = p.nP_ID and c.C_ID = %s",(session["c_id"],))
    # print(cnx.fetchall())
    data=[{'c_id':i[0],'np_id':i[1],'product_name':i[2],'product_price':i[3],'product_quantity':i[4],'total_price':i[5]} for i in cnx.fetchall()]
    cnx.close()
    print(data)
    return jsonify(data)

@app.route("/cartdata2",methods= ["GET", "POST"])
def get_data3():
    cnx=mysql.connection.cursor()
    cnx.execute("select c.C_ID, SUM(p.Price * c.Quantity) AS Grand_Total FROM cart c,N_Product p where c.P_ID = p.nP_ID and c.C_ID = %s GROUP BY c.C_ID",(session["c_id"],))
    data=[{'c_id':i[0],'grand_total':i[1]} for i in cnx.fetchall()]
    cnx.close()
    print(data)
    return jsonify(data)

@app.route("/cart",methods= ["POST","GET"])
def cart():
    if 'loggedin' in session:
        if request.method == 'POST':
            cnx=mysql.connection.cursor()
            cnx.execute("select c.C_ID, p.nP_ID, p.PName, p.Price, c.Quantity, (p.Price * c.Quantity) AS Total_Price FROM cart c,N_Product p where c.P_ID = p.nP_ID and c.C_ID = %s",(session["c_id"],))
            # print(cnx.fetchall())
            data=[{'c_id':i[0],'np_id':i[1],'product_name':i[2],'product_price':i[3],'product_quantity':i[4],'total_price':i[5]} for i in cnx.fetchall()]
            cnx.execute("select c.C_ID, SUM(p.Price * c.Quantity) AS Grand_Total FROM cart c,N_Product p where c.P_ID = p.nP_ID and c.C_ID = %s GROUP BY c.C_ID",(session["c_id"],))
            data2=[{'c_id':i[0],'grand_total':i[1]} for i in cnx.fetchall()]
            print(data)
            for i in data:
                cnx.execute("select max(o_id) from orders")
                m = [i[0] for i in cnx.fetchall()]
                cnx.execute("INSERT INTO orders(O_ID, O_date, O_price, C_ID, P_ID, A_ID,PAY_ID) VALUES (%s, CURRENT_DATE(), %s,%s,%s,2,0);",(m[0] + 1,data2[0]['grand_total'],session['c_id'],i['np_id'],))
                mysql.connection.commit()
            # print(cnx.fetchall())
            return redirect("/home")
            return render_template("home.html")
        return render_template("cart.html")
    return redirect(url_for('login'))

@app.route("/revenue2")
def get_dataa2():
    cnx=mysql.connection.cursor()
    cnx.execute('''SELECT o.O_Date, SUM(o.O_Price) AS Total_Revenue
FROM orders o,N_Product p , prod_cat pc
WHERE o.P_ID = p.NP_id
AND p.Cat_ID = pc.Cat_ID
AND YEAR(o.O_Date) = 2022
AND MONTH(o.O_Date) =12
AND pc.Cat_ID = 3
GROUP BY o.O_Date;''')
    data=[{'1: O_Date':i[0],'2: Total_Revenue':i[1]} for i in cnx.fetchall()]
    cnx.close()
    print(data)
    return jsonify(data)

@app.route("/revenue3")
def get_dataa3():
    cnx=mysql.connection.cursor()
    cnx.execute('''SELECT Cat_Name,pname, SUM(O_price) AS Total_Revenue
FROM Category, N_Product,orders
where Category.Cat_ID = N_Product.Cat_ID
and N_Product.NP_ID = orders.P_ID
GROUP BY Cat_Name,pname WITH ROLLUP;''')
    data=[{'1: Cat_Name':i[0],'2: pname':i[1],'3: Total_Revenue':i[2]} for i in cnx.fetchall()]
    cnx.close()
    print(data)
    return jsonify(data)


@app.route("/revenuecat")
def get_dataa1():
    cnx=mysql.connection.cursor()
    cnx.execute(''' SELECT pc.Cat_ID, 
       SUM(CASE WHEN MONTH(o.O_Date) = 1 THEN o.O_Price ELSE 0 END) AS January_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 2 THEN o.O_Price ELSE 0 END) AS February_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 3 THEN o.O_Price ELSE 0 END) AS March_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 4 THEN o.O_Price ELSE 0 END) AS April_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 5 THEN o.O_Price ELSE 0 END) AS May_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 6 THEN o.O_Price ELSE 0 END) AS June_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 7 THEN o.O_Price ELSE 0 END) AS July_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 8 THEN o.O_Price ELSE 0 END) AS August_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 9 THEN o.O_Price ELSE 0 END) AS September_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 10 THEN o.O_Price ELSE 0 END) AS October_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 11 THEN o.O_Price ELSE 0 END) AS November_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 12 THEN o.O_Price ELSE 0 END) AS December_Revenue
FROM orders o, N_Product p ,prod_cat pc
where o.P_ID = p.NP_id
AND p.Cat_ID = pc.Cat_ID
GROUP BY pc.Cat_ID
order by pc.Cat_ID;''')
    data=[{'1: CAT_ID':i[0],'2: January_Revenue':i[1],'3: February_Revenue':i[2],'4: March_Revenue':i[3],'5: April_Revenue':i[4],'6: May_Revenue':i[5],'7: June_Revenue':i[6],'8: July_Revenue':i[7],'9: August_Revenue':i[8],'9A: September_Revenue':i[9],'9B: October_Revenue':i[10],'9C: November_Revenue':i[11],'9D: December_Revenue':i[12]} for i in cnx.fetchall()] # need to edit this to meet requirment
    cnx.close()
    # print(data)
    return jsonify(data)

@app.route("/revenueq")
def get_dataa4():
    cnx=mysql.connection.cursor()
    cnx.execute('''SELECT YEAR(O_Date) AS Year, QUARTER(O_Date) AS Quarter, SUM(O_Price) AS Total_Revenue
FROM orders
GROUP BY YEAR(O_Date), QUARTER(O_Date) with rollup
order by YEAR(O_Date);''')
    data=[{'1: YEAR':i[0],'2: QUARTER':i[1],'3: Total_Revenue':i[2]} for i in cnx.fetchall()]
    cnx.close()
    print(data)
    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True)
