import logging
import logstash
import sys

host = '0.0.0.0'
port = 5000

test_logger = logging.getLogger('python-logstash-loggerrr')
test_logger.setLevel(logging.INFO)
#test_logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))
test_logger.addHandler(logstash.TCPLogstashHandler(host, port, tags=['django'],message_type='django', version=1))

test_logger.error('python-logstash: test logstash error message.')
test_logger.error('python-django: test logstash error message.')
test_logger.info('python-logstash: test logstash info message.')
test_logger.warning('python-logstash: test logstash warning message.')

#import requests

#res = requests.get('http://localhost:9200')

#print(res.content)

#test_logger.warning('python-logstash: test logstash warning message.')