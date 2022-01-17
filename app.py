from flask import Flask
from flask_cors import CORS
from flask import render_template ,flash
from flask import request,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,validators
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.mysql import MySQL 
from datetime import datetime
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
import pymysql




app = Flask(__name__)
#sqlite 
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db'

#mysql


db=SQLAlchemy(app)
migrate=Migrate(app,db)
app.config['SECRET_KEY']="my secret key"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #car = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    account=StringField("Account:",validators=[DataRequired(),validators.Length(3, 20)])
    password=StringField("Password:",validators=[DataRequired(),validators.Length(8, 20)])
    email=StringField("Email:",validators=[DataRequired()])
    submit=SubmitField("submit")

#shopcar   
"""@app.route("/shopcar/<int:id>",methods=['GET','POST'])
def shopcar(id):
    form=UserForm()
    car_to_update=Users.query.get_or_404(id)
    if request.method=="POST":
        car_to_update.car=request.form['car']
        try:
            db.session.commit()
            flash("successfully")
            return  render_template('/shopcar.html',
              form=form,
              car_to_update=car_to_update)
        except:
             flash("error")
             return  render_template('/shopcar.html',
              form=form,
              car_to_update=car_to_update)
    else:
         return  render_template('/shopcar.html',
            form=form,
            car_to_update=car_to_update)   
"""

#flask_login stuff
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='sign'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#create login form class
class NameForm(FlaskForm):
    account=StringField("Account:",validators=[DataRequired()])
    password=PasswordField("Password:",validators=[DataRequired()])
    submit1=SubmitField("Log in")
    submit=SubmitField("Sign Up")

#loginpage
@app.route("/sign",methods=['GET','POST'])
def sign():
    account=None
    password=None
    login=0
    form=NameForm()
    #validate form
    if form.validate_on_submit():
        account=form.account.data
        password=form.password.data
        success=Users.query.filter_by(account=form.account.data).first()
        if success is None:
            flash("account or password is incorrect!")
        else:
            success2=Users.query.filter_by(password=form.password.data).first()
            if success2 is None:
                flash("account or password is incorrect!")
            else:
                flash("Login Successfully!")
                login=1
        #account=form.account.data
        #password=form.password.data
        form.account.data=''
        form.password.data=''
        #flash("Login Successfully!")

    return  render_template("sign.html",
        account=account,
        password=password,
        form=form)


#signuppage
@app.route("/signup",methods=['GET','POST'])
def signup():
    account=None
    form=UserForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user=Users(account=form.account.data,password=form.password.data,email=form.email.data)
            flash("Account Added Successfully!")
            db.session.add(user)
            db.session.commit()
        else:
            flash("This email has already been used!")
        account=form.account.data
        form.account.data=''
        form.password.data=''
        form.email.data=''
        #flash("Account Added Successfully!")
    our_users=Users.query.order_by(Users.date_added)
    return  render_template('signup.html', form=form,account=account,our_users=our_users)


#homepage
@app.route("/")
def index():
    return  render_template('index.html')

@app.route("/index2/",methods=['GET','POST'])
#@login_required
def index2():
    form=UserForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(account=form.account.data).first()
        if user:
            login_user(user)
            return redirect(url_for('index2'))
        
    return  render_template('index2.html',form=form)


#about us page
@app.route("/about")
def about():
    return  render_template('/about.html')

@app.route("/about2")
def about2():
    return  render_template('/about2.html')


#shop car
@app.route("/shopcar")
def shopcar():
    return  render_template('/shopcar.html')

@app.route("/car")
def car():
    return  render_template('/car.html')


@app.route("/coupon")
def coupon():
    return  render_template('/coupon.html')


#search page
@app.route("/python")
def python():
    return  render_template('python.html')

@app.route("/python2")
def python2():
    return  render_template('python2.html')

@app.route("/pythondollar")
def pythondollar():
    return  render_template('pythondollar.html')

@app.route("/pythontime")
def pythontime():
    return  render_template('pythontime.html')

@app.route("/java")
def java():
    return  render_template('java.html')

@app.route("/java2")
def java2():
    return  render_template('java2.html')

@app.route("/linux")
def linux():
    return  render_template('linux.html')

@app.route("/english")
def english():
    return  render_template('english.html')


@app.route("/search1")
def search1():
    return  render_template('/search1.html')



#invalid url
@app.errorhandler(404)
def page_not_found(e):
    return  render_template('404.html'),404

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0') #Start server
