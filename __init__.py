from flask import Flask,render_template,request,redirect,url_for,flash
import runp
from passlib.hash import sha256_crypt
from flask_mail import Mail,Message
import random
import string
from labsql import *

app=Flask(__name__)
app.secret_key = "this is nothing but a secret key"
app.config['MAIL_SERVER']='smtp@gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='in.hodophile@gmail.com'
app.config['MAIL_PASSWORD']='rajatmanish'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mom0511@localhost/groot"
app.config["SQLALCHEMY_BINDS"]={
									"Teachers":"mysql+pymysql://root:mom0511@localhost/teachers",
									"Students":"mysql+pymysql://root:mom0511@localhost/students"
								}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db.app=app
#db.create_all()
db1.init_app(app)
db1.app=app
db2.init_app(app)
db2.app=app



def pass_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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

@app.route("/signup-page")
def signup_page():
    return render_template("select.html")

@app.route("/signup-page/Teacher")
def signupTeacher():
    return render_template("sign.html")

@app.route("/signup-page/Student")
def signupStudent():
    return render_template("signstu.html")



@app.route("/login/<string:type>",methods=["GET","POST"])
def login(type):
    try:
        if request.method=="POST":
            uname=request.form["username"]
            passwd=request.form["passwd"]
            if type=="Teacher":
                user=Teachers.query.filter_by(username=uname).all()
                if len(user)==0:
                    flash("No such Teacher Present!!!")
                    return redirect(url_for("home"))
                if sha256_crypt.verify(passwd,str(user[0].passwd)):
                    return render_template("teachers.html")
            else:
                user=Student.query.filter_by(username=uname).all()
                if len(user)==0:
                    flash("No such Teacher Present!!!")
                    return redirect(url_for("home"))
                if sha256_crypt.verify(passwd,str(user[0].passwd)):
                    return render_template("student.html")
        else:
            flash("Wrong Credentials")
            return redirect(url_for("login_sign_page"))
    except Exception as e:
        return "Some Error Occured"

@app.route("/signup/<string:type>",methods=["GET","POST"])
def signup(type):
    if request.method=="POST":
        if type=="Teacher":
            clgname=request.form["clgname"]
            tecname=request.form["tecname"]
            uname=request.form["username"]
            passwd=str(pass_generator)
            msg=Message('FROM Onlinelabs',sender='in.hodophile@gmail.com',recipients=[uname])
            msg.body="your password for first login is "+passwd
            mail.send(msg)
            passwd=sha256_crypt.encrypt(passwd)
            insert_techer_cred=TeachersCredentials(username=uname,password=passwd)
            db.session.add(insert_techer_cred)
            db.session.commit()
            user=TeachersCredentials.query.filter_by(username=uname).all()[0]
            insert_techer_detail=TeacherDetails(teacher_id=user.teacher_id,username=user.username,teacher_name=tecname,college_id=clgname.split("-")[-1])
            db1.session.add(insert_techer_detail)
            db1.session.commit()
            flash("Password for first login sent to your mail!!!")
            return redirect(url_for("login_sign_page"))
        if type=="Student":
			clgname=request.form["clgname"]
			stuname=request.form["stuname"]
			uname=request.form["username"]
			course=request.form["course"]
			sem=request.form["sem"]
			section=request.form["sec"]
			rollno=request.form["roll"]
			branch=request.form["branch"]
			passwd=str(pass_generator)
			#msg=Message('FROM Onlinelabs',sender='in.hodophile@gmail.com',recipients=[uname])
			#msg.body="your password for first login is "+passwd
			#mail.send(msg)
			passwd=sha256_crypt.encrypt(passwd)
			insert_stu_cred=StudentsCredentials(username=uname,password=passwd)
			db.session.add(insert_stu_cred)
			db.session.commit()
			user=StudentsCredentials().query.all()[0]
			insert_stu_detail=StudentDetails(student_id=user.student_id,username=user.username,student_name=stuname,college_id=clgname.split("-")[-1],course=course,sem=sem,sec=section,rollno=rollno)
			db2.session.add(insert_stu_detail)
			db2.session.commit()
			flash("Password for first login sent to your mail!!!")
			return redirect(url_for("login_sign_page"))



if __name__ == '__main__':
    app.run(debug="true",port=8000 )
