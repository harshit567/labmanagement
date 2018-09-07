from flask import Flask,render_template,request,redirect,url_for
import runp
from passlib.hash import sha256_crypt
from flask_mail import Mail,Message


app=Flask(__name__)

app.config['MAIL_SERVER']='smtp@gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='in.hodophile@gmail.com'
app.config['MAIL_PASSWORD']='rajatmanish'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

'''
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mom0511@localhost/groot"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db.app=app
db.create_all()
'''
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/run",methods=["GET","POST"])
def run():
    extention=request.form["ext"]
    name=request.form["filename"]
    code=request.form["code"]
    file_name=name+"."+extention
    f=open(file_name,"w")
    f.write(code)
    f.close()
    if extention == "java":
        output=runp.run_java(file_name)
        return output
    elif extention == "cpp":
        output=runp.run_cpp(file_name)
        return output
    elif extention == "c":
        output=runp.run_c(file_name)
        return output
    elif extention == "python":
        output=runp.run_python(file_name)
        return output
    elif extention == "sql":
        userdb="groot"
        password="mom0511"
        output=runp.run_mysql(code,userdb,password)
        return output

@app.route("/login-sign-page")
def login_sign_page():
    return render_template("login.html")

@app.route("/login",methods=["GET","POST"])
def login():
    try:
        if request.method=="POST":
            type=request.form["logintype"]
            uname=request.form["username"]
            passwd=request.form["passwd"]
            if type=="Teacher":
                user=Teachers.query.filter_by(username=uname).first()
                if user.username=="null":
                    flash("No such Teacher Present!!!")
                    return redirect(url_for("home"))
            else:
                user=Student.query.filter_by(username=uname).first()
            if sha256_crypt.verify(passwd,user.passwd):
                return render_template("student.html")
            else:
                flash("Wrong Credentials")
                return redirect(url_for("login_sign_page"))
    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run(debug="true",port=8000 )
