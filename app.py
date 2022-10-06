from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qatest.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String)
    gender = db.Column(db.String)
    dateadd = db.Column(db.DateTime, default=datetime.utcnow)
    meals = db.relationship('Meals',backref='all_meals')

class Meals(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.ForeignKey('users.id'))
    breakfast = db.Column(db.String)
    lunch = db.Column(db.String)
    dinner = db.Column(db.String)
    snacks = db.Column(db.String)
    drinks = db.Column(db.String)
    workout = db.relationship('Workouts',backref='all_workouts')

class Workouts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    meals = db.Column(db.ForeignKey('meals.id'))
    kickboxing = db.Column(db.String)
    boxing = db.Column(db.String)
    push_up = db.Column(db.String)
    pull_up = db.Column(db.String)
    
 
#db.create_all()
@app.route('/',methods=['GET','POST'])
def home_fun():
    if request.method == 'POST' and request.form.get('action') == 'Create':
        id = int(request.form.get('id'))
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        c_new = Users(id=id,fname=fname,lname=lname,email=email)
        db.session.add(c_new)
        db.session.commit()
        return redirect(url_for("home_fun"))


    if request.method == 'POST' and request.form.get('actions') == 'Search':
        search_query = request.form.get('email')
        data_to_show = Users.query.filter_by(name=search_query)
    else:
        data_to_show = Users.query.all()
    return render_template("home.html",list_of_data=data_to_show)

@app.route('/company/<int:id>')
def courses_fun(id):
    company_object = Users.query.get(id)
    return render_template("comany.html",data=company_object) 

@app.route('/',methods=['GET','POST'])
def update_fun():
    if request.method == 'POST' and request.form.get('action') == 'Update':
    
        db.session.commit_all()
        return redirect(url_for("update_fun"))

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)