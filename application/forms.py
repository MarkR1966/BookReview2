import g
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from application import db
from application.models import Books, Users, Authors


def validate_book(self, b_title):                             # Checks Title does not exist in Books table
    if b_title.data != g.def_b_Title:                   # is this the current title when updating
        book = Books.query.filter_by(b_Title=b_title.data).first()
        if book:
            raise ValidationError('Title already in use')


def validate_author(self, b_author):                    # check if author already exists in the authors table
    if b_author.data != g.def_b_Author:                 # has author changed
        if "UpdateBooksForm" in str(self):
            author = Authors.query.filter_by(a_Author=g.def_b_Author).first()
        else:
            author = Authors.query.filter_by(a_Author=b_author.data).first()
        if author:                                      # Does author exist?
            g.def_b_Author_id = author.id
        else:                                           # create if not exist
            author_data = Authors(
                a_Author=b_author.data,
            )
            db.session.add(author_data)
            db.session.commit()
            author_data = Authors.query.filter_by(a_Author=b_author.data).first()
            g.def_b_Author_id = author_data.id
    return True


def validate_email(self, u_email):                            # Checks Email address does not exist in the Users table
    check = True
    if current_user.is_authenticated:                   # is Current user logged in
        if u_email.data == current_user.email:          # is this the Current User email when updating
            check = False
    if check:
        user = Users.query.filter_by(u_email=u_email.data).first()
        if user:
            raise ValidationError('Email already in use')


def validate_user(self, u_name):                              # Checks Username does not exist in the Users table
    check = True
    if current_user.is_authenticated:                   # is Current user logged in
        if u_name.data == current_user.u_name:          # is this the Current Username
            check = False
    if check:
        user = Users.query.filter_by(u_name=u_name.data).first()
        if user:
            raise ValidationError('Username already in use')


class BooksForm(FlaskForm):                             # define Class that will be used for Books Form data
    b_Title = StringField(
        'Book Title',
        validators=[
            DataRequired(),                             #
            Length(min=1, max=30),
            validate_book
        ]
    )

    b_Author = StringField(
        'Author',
        validators=[
            DataRequired(),
            Length(min=1, max=30),
            validate_author
        ]
    )

    b_Publisher = StringField(
        'Publisher',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    b_Synopsis = StringField(
        'Synopsis',
        validators=[
            Length(min=0, max=300)
        ]
    )

    submit = SubmitField('Add Book Details')


class AuthorForm(FlaskForm):                            # define Class that will be used for Author Form data
    a_Author = StringField(
        'Author',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    submit = SubmitField('Add Author Details')


class RegistrationForm(FlaskForm):                      # define Class that will be used for Registration Form data
    u_name = StringField(
        'User Name',
        validators=[
            DataRequired(),
            Length(min=6, max=30),
            validate_user
        ]
    )
    u_email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            validate_email
        ]
    )
    u_password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=30)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('u_password')
        ]
    )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):                             # define Class that will be used for Login Form data
    u_email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    u_password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):                     # define Class that will be used for UpdateAccount Form data
    u_name = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ]
    )

    u_email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            validate_email
        ]
    )
    submit = SubmitField('Update')


class UpdateBooksForm(FlaskForm):                       # define Class that will be used for UpdateBooks Form data
    b_Title = StringField(
        'Book Title',
        validators=[
            DataRequired(),
            Length(min=1, max=30),
            validate_book
        ]
    )

    b_Author = StringField(
        'Author',
        validators=[
            DataRequired(),
            Length(min=1, max=30),
            validate_author
        ]
    )

    b_Publisher = StringField(
        'Publisher',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    b_Synopsis = StringField(
        'Synopsis',
        validators=[
            Length(min=0, max=300)
        ]
    )

    submit = SubmitField('Update Book Details')
