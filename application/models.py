from flask_login import UserMixin

from application import db, login_manager


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a_Author = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return ''.join(
            [
                'Author ID: ' + str(self.id) + '\n'
                'Author: ' + self.a_Author + '\n'
            ]
        )


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_Title = db.Column(db.String(30), nullable=False, unique=True)
    b_Publisher = db.Column(db.String(30), nullable=False)
    b_Synopsis = db.Column(db.String(300), nullable=True)
    b_Author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    books = db.relationship('Authors', backref=db.backref('a_author_id', lazy=True))

    def __repr__(self):
        return ''.join(
            [
                'Title: ' + self.b_Title + '\n'
                'Author ID: ' + str(self.b_Author_id) + '\n'
                'Publisher: ' + self.b_Publisher + '\n'
                'Synopsis: ' + self.b_Synopsis
            ]
        )


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(30), nullable=False, unique=True)
    u_email = db.Column(db.String(500), nullable=False, unique=True)
    u_password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return ''.join(
            [
                'UserID: ', str(self.id) + '\r\n'
                'User Name: ' + self.u_name + '\n'
                'Email: ', self.u_email
            ]
        )


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
