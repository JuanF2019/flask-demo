from flask import Flask, render_template, url_for, request
from datetime import datetime
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev'
)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

#Crear formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min=4,max=25)])
    password = PasswordField("Password", validators = [DataRequired(), Length(min=6,max=40)])
    submit = SubmitField("Register")

@app.route('/auth/register',methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        return f"Username: {username}, Contraseña: {password}"

    return render_template('auth/register.html',form=form)