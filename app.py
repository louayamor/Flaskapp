from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#returning a tmeplate by render template
#flash for flash messages
#redirect to handle redirection
from data import Articles
#importing the database
from flask_mysqldb import MySQL
# Imporing forms
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# Importing passwords' library
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Configuring Mysql
app.config('MYSQL_HOST') = 'localhost'
app.config('MYSQL_USER') = 'root'
app.config('MYSQL_PASSWORD') = '123456'
app.config('MYSQL_DB') = 'flaskapp'
# Mysql returns a tuple data type by default so we have to make it return a dictionary
app.config('MYSQL_CURSORCLASS') = 'Dictcursor'
# init MYSQL
mysql = MySQL(app)

Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('articles.html', id=id)

class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('Username',[validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=8, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('Confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        # We created this with the help of FlaskSQLDataBase documentation
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)",(name, email,username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in','success')

        redirect(url_for('index'))

        return render_template('register.html')
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

