from application import db, bcrypt
from application.models import Books, Users, Authors

db.drop_all()
db.create_all()
author = Authors(a_Author="Harry Turtledove")
book = Books(b_Title='The Two Georges', b_Author_id=1, b_Publisher='Hodder & Staughton.',
             b_Synopsis='Murder and political intrigue based in a modern day America that is still part of\
              the Greater British Empire')
hash_pw = bcrypt.generate_password_hash("12345678")
user = Users(u_name="MarkR1966", u_email="markrafferty27@gmail.com", u_password=hash_pw)

db.session.add(book)
db.session.add(user)
db.session.add(author)
db.session.commit()

