import json
import urllib2
import sys
import time
import base64


class Message:
	"""[summary]
	"""

	def __init__(self):
		self.url = 'http://localhost:8000/api/message/'
		self.api_user = ''
		self.api_password = ''
		self.base64auth = base64.encodestring('%s:%s' % (self.api_user, self.api_password)).replace('\n', '')


	def save(self, message, ip=None):
		data = {
			'ip': ip,
			'msg': message,
			'timestamp': time.time()
		}
		req = urllib2.Request(self.url)
		req.add_header('Content-Type', 'application/json')
		req.add_header('Authorization', "Basic %s" % self.base64auth)
		try:
			response = urllib2.urlopen(req, json.dumps(data))
			return json.loads(response.read())
		except Exception as e:
			print 'error: '+str(e)
			return None


if __name__ == '__main__':
	if len(sys.argv) >= 2:
		ms = Message()
		print ms.save(sys.argv[1], sys.argv[2])
	else:
		print 'usage: ' + sys.argv[0] + ' message [ip]'
