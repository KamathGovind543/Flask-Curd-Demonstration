from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.curd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Employee(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def __init__(self,name,email,phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def Index():
    all_Data = Employee.query.all()
    return render_template('index.html',Employee_Data = all_Data)

@app.route('/insert' , methods=['POST'])
def insert():
    if request.method == 'POST':    
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        recorded_data = Employee(name,email,phone)
        db.session.add(recorded_data)
        db.session.commit()

        flash("Data added Successfully")

        return redirect(url_for('Index'))

@app.route('/update' , methods=['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = Employee.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone =request.form['phone']

        db.session.commit()
        flash('Employee Updated Succssfully!')

        return redirect(url_for('Index'))


@app.route('/delete/<id>/',methods = ['GET','POST']) 
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete (my_data)
    db.session.commit()
    flash("Employee Deleted Successfully!")  

    
    return redirect(url_for('Index'))    

if __name__ == '__main__':
    app.run(debug=True)