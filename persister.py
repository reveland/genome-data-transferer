import datetime
import json

def persist(data, step, name):
	now = datetime.datetime.now()
	file_name = './data/%s_%s_%s.json' % (name, step, now.strftime("%Y-%m-%d_%H:%M:%S"))
	data.to_json(file_name, orient='records')
