from flask import Flask, render_template, url_for, request
from datetime import datetime
from wtforms.validators import DataRequired, Length
#flask --app hello --debug run debug allow for hot updates
#flask --app hello run
#Represents flask app
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev'
)

#Filtros personalizados
#@app.add_template_filter
def today(date):
    return date.strftime('%d-%m-%Y')
app.add_template_filter(today,"today")

#función personalizada
@app.add_template_global
def repeat(s,n):
    return s*n

#app.add_template_global(repeat,'repeat')

@app.route('/')
@app.route('/index')
def index():
    #name = None
    print(url_for('index'))
    print(url_for('hello3', name = 'Juan', age = 27))
    print(url_for('code',code='print("hola")'))

    name = 'Juan' 

    friends = ["Valentina","Alejandro","María","Jorge","Daniel"]

    date =  datetime.now()

    return render_template(
                "index.html",
                name=name,
                friends=friends,
                date = date
                )
'''repeat = repeat'''
@app.route('/')
#Each function must be unique else the first one is shown
def bye():#This function returns a view
    return '<h1>Start page</h1>'

#A data type for a value can be specified in the route as <type:var>
#Multiple value are separated by /
#string
#int
#float
#path
#uuid
@app.route('/hello/<name>')

@app.route('/hello3/<string:name>')
#Each route must be associated with a function
#To receive parameters from the URL the route must include
# a variable as <var> and the function must contain a parameter with the same name
def hello(name):#This function returns a view
    return f'<h1> hello {name} </h1>' 

@app.route('/hello2')
@app.route('/hello2/<string:name>')
@app.route('/hello2/<string:name>/<int:age>')
def hello2(name=None,age=None):
    if name == None and age == None:
        return "<h1> Hello World !</h1>"
    
    if age == None:
        return f'<h1> Hello, {name} </h1>'

    #How to make possible to print only age?
    if name == None:
        return f'<h1> Hello, double your age is {age}</h1>'

    return f'<h1>Hello {name}, you are {age} years old</h1>'
    

@app.route('/hello3')
@app.route('/hello3/<string:name>')
@app.route('/hello3/<string:name>/<int:age>')
@app.route('/hello3/<string:name>/<int:age>/<email>')
def hello3(name=None,age=None,email=None):
    my_data={
        'name': name,
        'age' : age,
        'email' : email
    }
    return render_template('hello.html',data=my_data)
    

from markupsafe import escape

#Use escape for security purposes
#Converts everything to text
@app.route('/code/<path:code>')
def code(code):
    return f'<code>{escape(code)}</code>'

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

    '''
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) >= 4 and len(username) <= 25 and len(password) >= 6 and len(password) <= 40:
            return f"Username:{username}, password: {password}"
        else:
            error = """Username must have between 4 and 25 characters and passsword between 6 and 40"""
            return render_template('auth/register.html', form=form, error=error)
    '''
    return render_template('auth/register.html',form=form)