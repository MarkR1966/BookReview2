import g
from application import app, db, bcrypt
from flask import render_template, redirect, url_for, request
from application.models import Books, Users, Authors
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import UpdateBooksForm, BooksForm, AuthorForm, UpdateAccountForm, LoginForm, RegistrationForm


def validate_author(b_author):                      # check if author already exists in the authors table
    author = Authors.query.filter_by(a_Author=b_author).first()
    if author:
        g.def_b_Author_id = author.id
        return True
    else:
        return False


@app.route('/', methods=['GET'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET'])
@app.route('/home')
@login_required
def home(page=1):
    per_page = 5
    book_data = Books.query.order_by(Books.b_Title).paginate(page, per_page, error_out=False)
    return render_template('home.html', title='Homepage', books=book_data)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
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
    form = BooksForm()
    if form.validate_on_submit():
        g.def_b_Title = form.b_Title.data
        g.def_b_Author = form.b_Author.data
        g.def_b_Publisher = form.b_Publisher.data
        g.def_b_Synopsis = form.b_Synopsis.data
        if validate_author(form.b_Author.data):
            book_data = Books(
                b_Title=form.b_Title.data,
                b_Author_id=str(g.def_b_Author_id),
                b_Publisher=form.b_Publisher.data,
                b_Synopsis=form.b_Synopsis.data
            )
            db.session.add(book_data)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('addauthor'))
    elif request.method == 'GET':
        form.b_Title.data = g.def_b_Title
        form.b_Author.data = g.def_b_Author
        form.b_Publisher.data = g.def_b_Publisher
        form.b_Synopsis.data = g.def_b_Synopsis
    return render_template('addbook.html', title='Add a Book', form=form)


@app.route('/addauthor', methods=['GET', 'POST'])
@login_required
def addauthor():
    form = AuthorForm()
    if form.validate_on_submit():
        g.def_b_Author = form.a_Author.data
        author_data = Authors(
            a_Author=form.a_Author.data,
        )
        db.session.add(author_data)
        db.session.commit()
        return redirect(url_for('add'))
    elif request.method == 'GET':
        form.a_Author.data = g.def_b_Author
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
        current_user.u_name = form.u_name.data
        current_user.u_email = form.u_email.data
        user = Users.query.filter_by(u_name=form.u_name.data).first()
        user.u_name = form.u_name.data
        user.u_email = form.u_email.data
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


@app.route('/updatebook/<bookid>', methods=['GET', 'POST'])
@login_required
def updatebook(bookid):
    form = UpdateBooksForm()
    if form.validate_on_submit():
        book = Books.query.filter_by(id=bookid).first()
        author = Authors.query.filter_by(id=book.b_Author_id).first()
        book.b_Title = g.def_b_Title = form.b_Title.data
        book.b_Publisher = g.def_b_Publisher = form.b_Publisher.data
        book.b_Synopsis = g.def_b_Synopsis = form.b_Synopsis.data
        author.a_Author = g.def_b_Author = form.b_Author.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        book = Books.query.filter_by(id=bookid).first()
        form.b_Title.data = g.def_b_Title = book.b_Title
        form.b_Author.data = g.def_b_Author = book.books.a_Author
        form.b_Publisher.data = g.def_b_Publisher = book.b_Publisher
        form.b_Synopsis.data = g.def_b_Synopsis = book.b_Synopsis
    return render_template('updatebook.html', title='Update a Book', form=form)


@app.route("/deletebook/<bookid>", methods=["GET", "POST"])
@login_required
def deletebook(bookid):
        book = Books.query.filter_by(id=bookid).first()
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('home'))
