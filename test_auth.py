import pickle
import os

password = "admin123"

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

def login(email, password):
    user = db.query(email)
    if user.password == password:
        return True
