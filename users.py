from flask import make_response, abort
from models import User, user_schema, users_schema
from config import db
from datetime import datetime

def get_users():
    users = User.query.all()
    return users_schema.dump(users)

def get_birthdays():
    users = User.query.all()
    user_dump = users_schema.dump(users)
    birthdays = []
    today = datetime.now().strftime("%Y-%m-%d")
    for user in user_dump:
        if user["birthday"] == today:
            user["age"] = datetime.now().year - int(user["birthday"].split("-")[0])
            birthdays.append(user)
    if len(birthdays) == 0:
        return abort(204, f"No birthdays today")
    return birthdays

def delete_user(user_id):
    user = User.query.filter(User.user_id == user_id).one_or_none()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    else:
        abort(404, f"User not found for Id: {user_id}")
        
    return make_response(f"User deleted", 200)


def get_user(user_id):
    user = User.query.filter(User.user_id == user_id).one_or_none()
    
    if user is not None:
        return user_schema.dump(user)
    else:
        abort(404, f"User not found for Id: {user_id}")

def update_tickets(user_id, body):
    existing_User = User.query.filter(User.user_id == user_id).one_or_none()
    if existing_User:
        operation = body['operation']
        amount = body['ticket_value']
        if operation == "add":
            existing_User.tickets += amount
        elif operation == "subtract":
            existing_User.tickets -= amount
        elif operation == "set":
            existing_User.tickets = amount
        else:
            abort(400, f"Invalid operation: {operation}")

        db.session.merge(existing_User)
        db.session.commit()
        return user_schema.dump(existing_User), 200
    else:
        abort(404, f"User with id {user_id} not found")

def get_tickets(user_id):
    existing_User = User.query.filter(User.user_id == user_id).one_or_none()
    if existing_User:
        return {"tickets": existing_User.tickets}
    else:
        abort(404, f"User with id {user_id} not found")      

def get_introduction(user_id):
    existing_User = User.query.filter(User.user_id == user_id).one_or_none()
    if existing_User:
        return [{"introduction_message_id": str(existing_User.introduction_message_id), "introduction_completed": existing_User.introduction_completed}], 200
    else:
        abort(404, f"User with id {user_id} not found")      

def new_user(body):
    existing_User = User.query.filter(User.user_id == body["user_id"]).one_or_none()

    if existing_User is None:
        body["created_at"] = str(datetime.now())
        body["tickets"] = 0
        body["introduction_message_id"] = None
        new_person = user_schema.load(body, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return user_schema.dump(new_person), 201
    else:
        abort(406, f"Invalid operation - User already exists")

def update_user(user_id, body):
    existing_User = User.query.filter(User.user_id == body["user_id"]).one_or_none()

    if existing_User is not None:
        modified_User = user_schema.load(body, session=db.session)
        existing_User.introduction_message_id = modified_User.introduction_message_id; 
        db.session.merge(existing_User)
        db.session.commit()
        return user_schema.dump(existing_User), 200
    else:
        abort(406, f"Invalid operation - User not found")




#curl -X PATCH "http://localhost:5000/api/users/tickets/161160003334438912" -H "apikey: 123" -H "Content-Type: application/json" -d "{\"operation\":\"add\",\"ticket_value\":1000}"

#curl -X GET "http://localhost:5000/api/users/tickets/161160003334438912" -H "apikey: 123"

#curl -X GET "http://localhost:5000/api/users/introductions/161160003334438912" -H "apikey: 123"

#curl -X GET "http://localhost:5000/api/users/161160003334438912" -H "apikey: 123"

#curl -X PUT "http://localhost:5000/api/users/create" -H "apikey: 123" -H "Content-Type: application/json" -d "{\"user_id\":\"16116000333443891\",\"name\":\"John Doe\",\"introduction_message_id\":123456, \"introduction_completed\":1,\"birthday\":\"01/01/2000\"}"

#curl -X DELETE "http://localhost:5000/api/users/161160003334438912 -H "apikey: 123"

#curl -X DELETE "http://localhost:5000/api/users/birthdays -H "apikey: 123"