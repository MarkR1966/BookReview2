from application import app, db, bcrypt
from flask import render_template, redirect, url_for, request
from application.forms import BooksForm, RegistrationForm, LoginForm, UpdateAccountForm
from application.models import Books, Users
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
@login_required
def home():
    book_data = Books.query.all()
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

        return redirect(url_for('home'))
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
        book_data = Books(
            b_Title=form.b_Title.data,
            b_Author_id=form.b_Author_id.data,
            b_Publisher=form.b_Publisher.data,
            b_Synopsis=form.b_Synopsis.data
        )
        db.session.add(book_data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('post.html', Title='Add a post', form=form)


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
        posts = Posts.query.filter_by(user_id=user)
        for post in posts:
                db.session.delete(post)
        account = Users.query.filter_by(id=user).first()
        logout_user()
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for('register'))
