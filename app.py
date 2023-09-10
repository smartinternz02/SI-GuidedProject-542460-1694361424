from flask import Flask, redirect, render_template,url_for, request
import ibm_db

app =  Flask(__name__)


# dsn_hostname = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
# dsn_uid = "vqs81643"
# dsn_pwd =  "7JI1Bl6aC0tLkslR"
# dsn_driver = "{IBM DB2 ODBC DRIVER}"
# dsn_database = "BLUDB"
# dsn_port = "30376"
# dsn_protocol = "TCPIP"

# dsn = ("DRIVER={0};""DATABASE={1};""HOSTNAME={2};""PORT={3};""PROTOCOL={4};""UID={5};""PWD={6};").format(dsn_driver,dsn_database,dsn_hostname,dsn_port,dsn_protocol,dsn_uid,dsn_pwd)
# print(dsn)

con = ibm_db.connect("DATABASE=BLUDB; HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; PORT=30376; PROTOCOL=TCPIP; UID=vqs81643; PWD=7JI1Bl6aC0tLkslR;SECURITY=SSL; SSLSERVERCERTIFICATE=DigiCertGlobalRootCA.crt;", "", "")
# ibm_db.connect(dsn,"","")
# print(con)
print(ibm_db.active(con))
@app.route('/')
def index(name=None):
    return render_template('index.html',name=name)

@app.route('/contact')
def contact(name=None):
    return render_template('contact.html',name=name)

@app.route('/profile/student')
def student_page():
    return "<h1>STUDENT PAGE</h1>"

@app.route('/profile/faculty')
def faculty_page():
    return "<h1>FACULTY PAGE</h1>"

@app.route('/profile/admin')
def admin_page():
    return "<h1>ADMIN PAGE</h1>"

@app.route('/login', methods = ["GET","POST"])
def login(name=None):
    if request.method == "POST":
        uname = request.form['username']
        pwd = request.form['password']
        print(uname,pwd)
        sql = 'SELECT * FROM REGISTER WHERE USERNAME = ? AND PASSWORD = ?'
        stmt = ibm_db.prepare(con,sql)
        ibm_db.bind_param(stmt,1,uname)
        ibm_db.bind_param(stmt,2,pwd)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)
        print(data)
        if data==False:
            msg="INVALID CREDENTIALS"
            return render_template("login.html",login_message=msg)
        else:
            role = data['ROLE']
            if role==0:
                return render_template('student_profile.html')
            elif role==1:
                return render_template('profile.html')
            elif role==2:
                return render_template('faculty_profile.html')
            else:
                pass

    return render_template('login.html',name=name)

@app.route('/addStudent', methods = ["GET","POST"])
def addStudent():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        uname = request.form['username']
        pwd = request.form['password']
        role = 0

        sql = "INSERT INTO REGISTER VALUES(?,?,?,?,?)"
        stmt = ibm_db.prepare(con,sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.bind_param(stmt,2,uname)
        ibm_db.bind_param(stmt,3,email)
        ibm_db.bind_param(stmt,4,pwd)
        ibm_db.bind_param(stmt,5,role)

        sql1 = 'SELECT * FROM REGISTER WHERE EMAILID = ?'
        stmt1 = ibm_db.prepare(con,sql1)
        ibm_db.bind_param(stmt1,1,email)
        ibm_db.execute(stmt1)
        data = ibm_db.fetch_assoc(stmt1)
        if data == False:
            res = ibm_db.execute(stmt)
            if res:
                msg=f"Hello {name.upper()} Registration Done!"
                return render_template("profile.html",registration_message=msg)
        else:
            msg = "USER already registered"
            return render_template("profile.html",registration_message=msg)        
        
    return render_template('profile.html')

@app.route('/profile')
def profile(name=None):
    return render_template('profile.html',name=name)

if __name__  == "__main__":
    app.run(debug=True)