from wtforms import ValidationError

from application import app, db, bcrypt
from flask import render_template, redirect, url_for, request
from application.forms import BooksForm, RegistrationForm, LoginForm, UpdateAccountForm, AuthorForm
from application.models import Books, Users, Authors
from flask_login import login_user, current_user, logout_user, login_required


def_b_Title = ""
def_b_Author = ""
def_b_Publisher = ""
def_b_Synopsis = ""
def_b_Author_id = 0


def validate_email(email, page):
    if page != 'register' and email == current_user.u_email:
        return True
    else:
        user = Users.query.filter_by(u_email=email).first()
        if user:
            return False
        else:
            return True


def validate_user(user):
        user = Users.query.filter_by(u_name=user).first()
        if user:
            return False
        else:
            return True


def validate_author(b_author):
    global def_b_Authors_id
    author = Authors.query.filter_by(a_Author=b_author).first()
    def_b_Author_id = Authors.id
    if author:
        return True
    else:
        return False


@app.route('/')
@app.route('/home')
@login_required
def home():
    book_data = Books.query.all()
    return render_template('home.html', title='Homepage', books=book_data)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/emaildup/<word>')
def emaildup(word):
    return render_template('emaildup.html', title='Email Error',para1=word)


@app.route('/userdup/<word>')
def userdup(word):
    return render_template('userdup.html', title='User Error',para1=word)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if not validate_email(form.u_email.data, "register"):
            return redirect(url_for('emaildup', word='register'))
        elif not validate_user(form.u_name.data):
            return redirect(url_for('userdup', word='register'))
        else:
            hash_pw = bcrypt.generate_password_hash(form.u_password.data)

            user = Users(u_name=form.u_name.data, u_email=form.u_email.data, u_password=hash_pw)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(u_email=form.u_email.data).first()
        if user and bcrypt.check_password_hash(user.u_password, form.u_password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home')
    return render_template('login.html', title='Login', form=form)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    global def_b_Title, def_b_Author, def_b_Publisher, def_b_Synopsis
    form = BooksForm()
    if form.validate_on_submit():
        def_b_Title = form.b_Title.data
        def_b_Author = form.b_Author.data
        def_b_Publisher = form.b_Publisher.data
        def_b_Synopsis = form.b_Synopsis.data
        if validate_author(form.b_Author.data):
            book_data = Books(
                b_Title=form.b_Title.data,
                b_Author_id=def_b_Author_id,
                b_Publisher=form.b_Publisher.data,
                b_Synopsis=form.b_Synopsis.data
            )
            db.session.add(book_data)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('addauthor'))
    elif request.method == 'GET':
        form.b_Title.data = def_b_Title
        form.b_Author.data = def_b_Author
        form.b_Publisher.data = def_b_Publisher
        form.b_Synopsis.data = def_b_Synopsis
    return render_template('addbook.html', title='Add a Book', form=form)


@app.route('/addauthor', methods=['GET', 'POST'])
@login_required
def addauthor():
    global def_b_Author
    form = AuthorForm()
    if form.validate_on_submit():
        def_b_Author = form.a_Author.data
        author_data = Authors(
            a_Author=form.a_Author.data,
        )
        db.session.add(author_data)
        db.session.commit()
        return redirect(url_for('add'))
    elif request.method == 'GET':
            form.a_Author.data = def_b_Author
    return render_template('addauthor.html', title='Add an Author', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if not validate_email(form.u_email.data, "account"):
            return redirect(url_for('emaildup', word='account'))
        elif not validate_user(form.u_name.data):
            return redirect(url_for('userdup', word='account'))
        else:
            current_user.u_name = form.u_name.data
            current_user.u_email = form.u_email.data
            db.session.commit()
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.u_name.data = current_user.u_name
        form.u_email.data = current_user.u_email
    return render_template('account.html', title='Account', form=form)

@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
        user = current_user.id
        account = Users.query.filter_by(id=user).first()
        logout_user()
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for('register'))
