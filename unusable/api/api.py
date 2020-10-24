# ==============================================================================
# IMPORTS
# ==============================================================================
import logging
import time
import datetime

from flask import Flask, Response, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_sqlalchemy import SQLAlchemy

from collections import defaultdict
# =============================================================================
# GLOBALS
# =============================================================================
JWT_VERIFY_EXPIRATION = False

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# ==============================================================================
# CLASSES MODEL
# ==============================================================================
class ApiMessage(db.Model):
    """class that represents the Message, a copy of it in the Django application
    """
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    timestamp = db.Column(db.String(30), default=time.time)
    msg = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    read_in = db.Column(db.DateTime, default=datetime.datetime.now)
    read_by_id = db.Column(db.Integer)

    @property
    def serialize(self):
        """Return object data in easily serializable format
        """
        return {'id': self.id, 'subject': self.subject, 'timestamp': self.timestamp,
                'msg': self.msg, 'read': self.read, 'deleted': self.deleted,
                'read_in': self.read_in, 'read_by_id': self.read_by_id}

    def __repr__(self):
        return f'<Message: {self.subject}:{self.msg[:25]}>'

class ApiComment(db.Model):
    """class that represents a comment on an existing message
    """
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer)
    comment = db.Column(db.String(254))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    commented_by_id = db.Column(db.Integer)

    @property
    def serialize(self):
        """Return object data in easily serializable format
        """
        return {'id': self.id, 'message_id': self.message_id, 'comment': self.comment,
                'commented_by_id': self.commented_by_id, 'created_at': self.created_at,
                'updated_at': self.updated_at}

    def __repr__(self):
        return f'<Comment: {self.message.id}:{self.comment[:30]}>'

class User(object):
    """Class that represents a user
    in the future it will be implemented from a database
    """
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

# User lists that the API allows authentication
users = [
    User(1, 'api', 'e7f6454c-6d1d-443e-ba8f-a08739724ce1'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

# =============================================================================
#  FUNCTIONS
# =============================================================================
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

def save(obj):
    """save object to database
    Args:
        obj ([type]): [ApiMessage or ApiComment]
    Returns:
        [dict]: [{'code': int, 'msg': str, 'data': dict or str}]
    """
    db.session.add(obj)
    try:
        db.session.commit()
    except Exception as err:
        return jsonify({'code': 500, 'msg': 'bad', 'data': err})
    return jsonify({'code': 200, 'msg': 'successful', 'data': obj.serialize})

jwt = JWT(app, authenticate, identity)

# =============================================================================
#  ROUTES APP
# =============================================================================
@app.route('/')
def status():
    """Index route to check if api is active
    Returns:
        [dict]: [status]
    """
    return jsonify({'status': 'up'})

@app.route('/version', methods=['POST', 'GET'])
@jwt_required()
def version():
    """Version of the libraries used in the api
    Returns:
        [dict]: [versions]
    """
    return jsonify({'app': '1.0.0', 'datail': {
        'flask': {
            'Flask': '1.1.2', 'Flask-JWT': '0.3.2'},
        'python': '3.8.3'
        }})

@app.route('/message', methods=['POST'])
@jwt_required()
def new_message():
    """Create a new message
    Returns:
        [dict]: [{'code': int, 'msg': str, 'data': dict or str}]
    """
    content = defaultdict(None, request.get_json())
    if (content.get('subject') is None) or (content.get('msg') is None):
        return jsonify({'code': 400, 'msg': 'bad args'})
    msg = ApiMessage(subject=content.get('subject'), msg=content.get('msg'),
        timestamp=content.get('timestamp') or str(time.time()))
    return save(msg)

@app.route('/comment', methods=['POST'])
@jwt_required()
def new_comment():
    """Create a comment on a message
    Returns:
        [dict]: [{'code': int, 'msg': str, 'data': dict or str}]
    """
    content = defaultdict(None, request.get_json())
    if (content.get('message') is None) or (content.get('comment') is None):
        return jsonify({'code': 400, 'msg': 'bad args'})
    comment = ApiComment(message_id=int(content.get('message')), comment=content.get('comment'))
    return save(comment)

@app.route('/list', methods=['GET'])
@jwt_required()
def list_message():
     """Lists all messages in the database
    Returns:
        [dict]: [all messages]
    """
    messages = [msg.serialize for msg  in ApiMessage.query.all()]
    return jsonify({'data': messages})

@app.route('/comments', methods=['GET'])
@jwt_required()
def list_comments():
    """Lists all comments in the database
    Returns:
        [dict]: [all comments]
    """
    comments = [msg.serialize for msg  in ApiComment.query.all()]
    return jsonify({'data': comments})
