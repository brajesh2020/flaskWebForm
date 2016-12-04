from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, ValidationError
from flask import Flask, flash, redirect, render_template, request, session, abort
import re
import os
engine = create_engine('mysql+mysqlconnector://root:@localhost/test', echo=True)

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


def testPassword(form, field):
    patern = "[A-Za-z0-9@#$%^&+=]{8,}"
    result = re.findall(patern, field.data)
    if result:
        print('Valid password')
    else:
        raise ValidationError('Password not valid')
        #print('Password not valid')


def testEmail(form, field):
    patern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$"
    result = re.findall(patern, field.data)
    if result:
        print('Email is valid')
    else:
        raise ValidationError('Email not valid')
        #print('Wrong email')


class ReusableForm(Form):
    name = TextAreaField('Name:', validators=[validators.required()])
    email = TextAreaField('email', validators=[validators.required(), testEmail])
    password = TextAreaField('password', validators=[validators.required(), testPassword])


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('hello.html')
    else:
        return "Hello Boss!"


@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['name'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.name.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(name, " ", email, " ", password)

        if form.validate():
            # Save the comment here.
            Session = sessionmaker(bind=engine)
            s = Session()
            user = User(request.form['name'], request.form['email'], request.form['password'])
            s.add(user)
            s.commit()
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    app.run()