from db import  db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__="user"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    username=db.Column(db.String(10),nullable=False)
    password=db.Column(db.String(125),nullable=False)
    def __init__(self,*args,**kwargs):
        id=kwargs.get("id")
        username = kwargs.get("username")
        password = kwargs.get("password")
        self.password = generate_password_hash(password)
        self.id=id
        self.username=username

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class RequestList(db.Model):
    __tablename__="RequestList"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    request_url=db.Column(db.String(100),nullable=False)
    request_type=db.Column(db.String(10),nullable=False)
    request_header=db.Column(db.String(1000),nullable=False)
    datatype=db.Column(db.String(50))
    request_data=db.Column(db.String(1000))
    request_status=db.Column(db.String(10),nullable=False)
    tasktime=db.Column(db.String(215), nullable=False)


class TaskList(db.Model):
    __tablename__="TaskList"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    Request_id=db.Column(db.INTEGER,nullable=False)
