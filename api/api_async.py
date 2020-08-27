import asyncio
import socket
import io
import sys
import logging

from flask import Flask, Response, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


host = 'localhost'
port = 9527

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(False)
s.bind((host, port))
s.listen(10)

loop = asyncio.get_event_loop()

class WSGIServer(object):

    def __init__(self, sock, app):
        self._sock = sock
        self._app = app
        self._header = []

    def parse_request(self, req):
        """ HTTP Request Format:

        GET /hello.htm HTTP/1.1\r\n
        Accept-Language: en-us\r\n
        ...
        Connection: Keep-Alive\r\n
        """
        # bytes to string
        req_info = req.decode('utf-8')
        first_line = req_info.splitlines()[0]
        method, path, ver = first_line.split()
        return method, path, ver

    def get_environ(self, req, method, path):
        env = {}

        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = req
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False

        # Required CGI variables
        env['REQUEST_METHOD']    = method    # GET
        env['PATH_INFO']         = path      # /hello
        env['SERVER_NAME']       = host      # localhost
        env['SERVER_PORT']       = str(port) # 9527
        return env

    def start_response(self, status, resp_header, exc_info=None):
        header = [('Server', 'WSGIServer 0.2')]
        self.headers_set = [status, resp_header + header]

    async def finish_response(self, conn, data, headers):
        status, resp_header = headers

        # make header
        resp = 'HTTP/1.1 {0}\r\n'.format(status)
        for header in resp_header:
            resp += '{0}: {1}\r\n'.format(*header)
        resp += '\r\n'

        # make body
        resp += '{0}'.format(data)
        try:
            await loop.sock_sendall(conn, str.encode(resp))
        finally:
            conn.close()

    async def run_server(self):
        while True:
            conn, addr = await loop.sock_accept(self._sock)
            loop.create_task(self.handle_request(conn))

    async def handle_request(self, conn):
        # get request data
        req = await loop.sock_recv(conn, 1024)
        if req:
            method, path, ver = self.parse_request(req)
            # get environment
            env = self.get_environ(req, method, path)
            # get application execute result
            res = self._app(env, self.start_response)
            res = [_.decode('utf-8') for _ in list(res)]
            res = ''.join(res)
            loop.create_task(self.finish_response(conn, res, self.headers_set))


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/')
def index():
    return Response("Hello WSGI", mimetype="text/plain")

@app.route('/status', methods=['POST', 'GET'])
@jwt_required()
def status():
    pass


server = WSGIServer(s, app.wsgi_app)
try:
    loop.run_until_complete(server.run_server())
except (BlockingIOError, KeyboardInterrupt):
    sys.stdout.write('\rclose web server.')
except Exception as err:
    logging.critical(err)
finally:
    loop.close()

# Then open browser with url: localhost:9527/hello
