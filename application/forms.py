from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from flask_login import current_user

class BooksForm(FlaskForm):
    b_Title = StringField(
        'Book Title',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    b_Author = StringField(
        'Author',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
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

    # def validate_author(self, b_Author):
    #     author = Authors.query.filter_by(AUthor=b_Author.data).first()
    #
    #     if author:
    #         raise ValidationError('Author does not exist')


class AuthorForm(FlaskForm):
    a_Author = StringField(
        'Author',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    submit = SubmitField('Add Author Details')


class RegistrationForm(FlaskForm):
    u_name = StringField(
        'User Name',
        validators=[
            DataRequired(),
            Length(min=6, max=30)
        ]
    )
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
            DataRequired(),
            Length(min=8, max=30)
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('u_password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, u_email):
        user = Users.query.filter_by(u_email=u_email.data).first()

        if user:
            raise ValidationError('Email already in use')



    # def validate_user(self, u_name):
    #     user = Users.query.filter_by(u_name=u_name.data).first()
    #
    #     if user:
    #         raise ValidationError('Username already in use')
    #
    #
class LoginForm(FlaskForm):
    u_email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    u_password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    u_name = StringField('Username',
            validators = [
                DataRequired(),
                Length(min=4, max=30)
            ]
    )

    u_email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    submit = SubmitField('Update')
