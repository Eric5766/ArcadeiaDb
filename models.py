from datetime import datetime
from config import db, ma

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.VARCHAR(20), nullable=False, primary_key=True, unique=True)
    name = db.Column(db.VARCHAR(20))
    tickets = db.Column(db.Integer, default=0)
    birthday = db.Column(db.Text)
    introduction_completed = db.Column(db.Integer, nullable=False, default=0)
    introduction_message_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

user_schema = UserSchema()
users_schema = UserSchema(many=True)