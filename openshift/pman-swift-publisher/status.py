import json
import sys

jdata = sys.stdin.read()
data = json.loads(jdata)

# Check if the image processing container is still running
if 'status' in data and 'containerStatuses' in data['status']:
	for status in data['status']['containerStatuses']:
	    if ('name' in status) and (status['name'] != 'publish'):
	      if ('state' in status) and ('terminated' in status['state']) and (status['state']['terminated']):
	        exit(0)

exit(1)
