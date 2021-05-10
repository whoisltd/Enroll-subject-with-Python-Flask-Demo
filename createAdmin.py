from app.models import Admin, User
from app import db
newUser = Admin(user_code = "12345678", name = "admin", email = "tiendat.le129@gmail.com", password="12345678")
newUser.set_password("12345678")
db.session.add(newUser)
db.session.commit()
