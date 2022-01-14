# Imports for API
import requests
import os
import hashlib
import csv
import json
import io
from dotenv import load_dotenv

# Imports for Pymongo
import pymongo
from bson.json_util import dumps


# Get secrets from dotenv
SECRET_USER = os.getenv("MONGODBUSER")
SECRET_PASS = os.getenv("MONGODBPASS")


# Connect to my MongoClient using the database username and password of an Atlas user that was created
my_mongo_client = pymongo.MongoClient('mongodb+srv://{SECRET_USER}:{SECRET_PASS}@cluster0.9ptvo.mongodb.net/Cluster0?retryWrites=true&w=majority')

my_mongo_db = my_mongo_client['Bat_DB']
my_mongo_collection = my_mongo_db['bat_test_collection']


def get_json_response(study_id):
	"""
	Returns the JSON Response based on the study_id from Movebank's database
	"""
	gps_events = get_individual_events(study_id, 653)
	json_response = gps_events
	# json_response = convert_to_json_string(gps_events)
	return json_response


def get_individual_events(study_id, sensor_type_id):
	"""
	Returns a List, based on various params such as entity_type, sensor_type, the study_id, etc from Movebank's database
	"""
	params = (
		('entity_type', 'event'), 
		('study_id', study_id), 
		('sensor_type_id', sensor_type_id), 
		('attributes', 'all')
	)
	events = call_movebank_api(params)
	if len(events) > 0:
		return list(csv.DictReader(io.StringIO(events), delimiter=','))
	return []


def call_movebank_api(params):
	"""
	Authenticate with Movebank API and return the Response content
	"""
	response = requests.get('https://www.movebank.org/movebank/service/direct-read', 
		params=params,
		auth=(os.getenv("MBUSER"),
		os.getenv("MBPASS"))
	)

	if response.status_code == 200:
		if '📰 License Terms:' in str(response.content):

			hash = hashlib.md5(response.content).hexdigest()
			params = params + (('license-md5', hash),)

			response = requests.get('https://www.movebank.org/movebank/service/direct-read',
									params=params,
									cookies=response.cookies,
									auth=(os.getenv("MBUSER"), os.getenv("MBPASS"))
									)
			if response.status_code == 403: 
				print("📛 Incorrect hash")
				return ''
		return response.content.decode('utf-8')
	print(str(response.content))
	return ''


def convert_to_json_string(l):
	"""
	Converts to JSON String
	"""
	return json.dumps(l, indent=2)


def write_json_to_file(data):
	"""
	Writes the data to output.json file and prettifies it
	"""
	with open('output.json', 'w') as f:
		json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ':'))


# Call to get user name & pass from .env file
load_dotenv()


# JSON Data is returned based on the Study ID that's passed
# Study ID: 312057662, is for Free-Tailed Bats 
# (https://www.movebank.org/cms/webapp?gwt_fragment=page=studies,path=study312057662)
bat_data = get_json_response(312057662)


# Rename JSON keys
# bat_data_time_series = bat_data.replace('individual_local_identifier','bat_id').replace('tag_local_identifier','tag_id')


# Call to prettify JSON and put it in a separate file
write_json_to_file(bat_data)


# Mongoimport is a command line tool to import JSON, CVS into a MongoDB Collection
# Since its a command line tool, use os.system to run it within Python
# Docs: https://docs.mongodb.com/database-tools/mongoimport/
# Ref: https://stackoverflow.com/questions/38700051/call-mongoimport-from-python-script
os.system(f'mongoimport --uri "mongodb+srv://{SECRET_USER}:{SECRET_PASS}@cluster0.9ptvo.mongodb.net/Bat_DB?retryWrites=true&w=majority" --collection Bat_Collection --drop --file ./output.json --jsonArray')
