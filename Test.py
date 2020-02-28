from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.secret_key = 'sjbsjubwubbajbsdjfhvelhvalhvdhbdsahbelen'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/test'

db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = 'employee_flask'
    eno = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(35))
    uname = db.Column(db.String(35))
    pwd = db.Column(db.String(35))
    addr = db.Column(db.String(35))

    def __init__(self, ename, uname, pwd, addr):
        self.ename = ename
        self.uname = uname
        self.pwd = pwd
        self.addr = addr


@app.route('/')
def m1():
    return render_template("login.html")


@app.route('/log', methods=['POST'])
def log():
    if(request.method == 'POST'):
        name = request.form['txtuname']
        pword = request.form['txtpassword']
        emp = Employee.query.filter(
            Employee.uname == name, Employee.pwd == pword).first()
        empdetail = {'eno': emp.eno, 'ename': emp.ename,
                     'uname': emp.uname, 'pwd': emp.pwd, 'addr': emp.addr}
        if emp != None:
            session['emp'] = json.dumps(empdetail)
            # return redirect(url_for('show'))
            return render_template('success.html', emp=emp)
        return redirect('/')


@app.route('/reg', methods=['GET', 'POST'])
def save():
    if(request.method == 'POST'):
        emp = Employee(request.form['txtname'], request.form['txtusername'],
                       request.form['txtpassword'], request.form['txtaddress'])

        db.session.add(emp)
        db.session.commit()

        return render_template("login.html")
    else:
        return render_template("register.html")

# Read Data
@app.route('/show')
def show():
    eList = Employee.query.all()
    return render_template("success.html", elst=eList)

# Delete Data
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('show'))

# Edit Data
@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    emp = Employee.query.get(id)
    return render_template("update.html", e=emp)


@app.route('/updatedata', methods=['POST'])
def update():
    emp = Employee(request.form.get('txtUename', False), request.form.get(
        'txtUuname', False), request.form.get('txtUpassword', False), request.form.get('txtUaddr', False))
    eno = request.form.get('txtUeno', False)
    # db.session.add(emp)
    db.session.query(Employee).filter(Employee.eno == eno).update(
        {Employee.ename: emp.ename, Employee.uname: emp.uname, Employee.pwd: emp.pwd, Employee.addr: emp.addr})
    db.session.commit()
    return redirect('show')


if(__name__ == '__main__'):
    db.create_all()
    app.run(debug=True)
