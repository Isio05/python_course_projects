from database import Database
from user import User
from constants import USER, PASSWORD

Database.initialise(user=USER, password=PASSWORD, database='Learning', host='localhost')

my_user = User(first_name='Ireneusz', last_name='Larysz', email='irenusz@larysz.com', id=None)

my_user.save_to_db()

user_from_db = User.load_from_db_by_email('irenusz@larysz.com')

print(user_from_db)
