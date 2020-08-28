import json
import urllib2
import sys
import time
import base64
import argparse

URL_BASE = 'http://localhost:8000'

class Message:
    """[summary]
    """

    def __init__(self, user=None, passwd=None):
        self.api_user = user or ''
        self.api_password = passwd or ''
        self.base64auth = base64.encodestring('%s:%s' % (self.api_user, self.api_password)).replace('\n', '')


    def new_msg(self, message, subject):
        data = {'subject': subject, 'msg': message, 'timestamp': time.time()}
        return self._post(data, '/api/message/')

    def new_comment(self, id_msg, comment):
        data = {"message": id_msg, "comment": comment}
        return self._post(data, '/api/comment/')
    
    def _post(self, data, url):
        req = urllib2.Request(URL_BASE+url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', "Basic %s" % self.base64auth)
        try:
            response = urllib2.urlopen(req, json.dumps(data))
            return json.loads(response.read())
        except Exception as e:
            print 'error: '+str(e)
        return None


class MSGArgumentParser(argparse.ArgumentParser):
    """A specialised argument parser to define common arguments
    """
    def __init__(self, *args, **kwargs):
        self._banner = kwargs.get('banner')
        if self._banner:
            del kwargs['banner']
        super(MSGArgumentParser, self).__init__(*args, **kwargs)
        # self.add_argument('-d', '--debug', action='store_true', help="enable debug messages")

    def parse_args(self):
        """Print the banner, parse arguments and configure some helpers using generic arguments
        """
        if self._banner:
            print(self._banner)
        args = super(MSGArgumentParser, self).parse_args()
        return args

def message(ms, args):
    """send message to API
    """
    print ms.new_msg(args.message, args.subject)

def comment(ms, args):
    """comment on existing message
    """
    print ms.new_comment(args.id, args.comment)

def setup_message(subparsers):
    parser = subparsers.add_parser('new', help="send a new message")

    parser.add_argument('subject', help="message subject")
    parser.add_argument('message', help="the message you want to send")
    parser.add_argument('-u', '--user-id', metavar='user_id', type=int, help="user id commenting")

    parser.set_defaults(func=message)


def setup_comment(subparsers):
    parser = subparsers.add_parser('comment', help="add comment to an already sent message")

    parser.add_argument('id', type=int, help="id of the message you want to comment")
    parser.add_argument('comment', help="comment you want to add the message")

    parser.set_defaults(func=comment)


if __name__ == '__main__':
    parser = MSGArgumentParser(description="script for sending messages and comments")

    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True

    # -- add subparsers
    setup_message(subparsers)
    setup_comment(subparsers)

    args = parser.parse_args()

    ms = Message()
    args.func(ms, args)
