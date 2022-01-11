import requests
import os
import hashlib
import csv
import json
import io
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def callMovebankAPI(params):
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


def getStudies():
    studies = callMovebankAPI((
        ('entity_type', 'study'), 
        ('i_can_see_data', 'true'), 
        ('there_are_data_which_i_cannot_see', 'false')
        ))
    if len(studies) > 0:
        # parse raw text to dicts
        studies = csv.DictReader(io.StringIO(studies), delimiter=',')
        return [s for s in studies if s['i_can_see_data'] == 'true' and s['there_are_data_which_i_cannot_see'] == 'false']
    return []


def getStudiesBySensor(studies, sensorname='GPS'):
    return [s for s in studies if sensorname in s['sensor_type_ids']]


def getIndividualsByStudy(study_id):
    individuals = callMovebankAPI((
        ('entity_type', 'individual'), 
        ('study_id', study_id)
        ))
    if len(individuals) > 0:
        return list(csv.DictReader(io.StringIO(individuals), delimiter=','))
    return []

# 635 is the ID for GPS sensors
def getIndividualEvents(study_id, sensor_type_id=653):
    params = (
        ('entity_type', 'event'), 
        ('study_id', study_id), 
        ('sensor_type_id', sensor_type_id), 
        ('attributes', 'all')
    )
    events = callMovebankAPI(params)
    if len(events) > 0:
        return list(csv.DictReader(io.StringIO(events), delimiter=','))
    return []


def transformRawGPS(gpsevents):

    def transform(e):
        try:
            if len(e['location_lat']) > 0:
                e['location_lat'] = float(e['location_lat'])
            if len(e['location_long']) > 0:
                e['location_long'] = float(e['location_long'])
        except:
            print("Could not parse long/lat.")
        return e['timestamp'], e['deployment_id'], e['location_lat'], e['location_long']

    return [transform(e) for e in gpsevents]


def convertToJson(l):
    return json.dumps(l, indent=2)


if __name__ == "__main__":

    # allstudies = getStudies()
    # gpsstudies = getStudiesBySensor(allstudies, 'GPS')
    # convertToJson(gpsstudies)


    # individuals = getIndividualsByStudy(study_id=9493874)
    # convertToJson(individuals)


    # individuals = getIndividualsByStudy(study_id=202883676)
    # convertToJson(individuals)


    def getFoxData():
        gpsevents = getIndividualEvents(study_id=202883676, sensor_type_id=653)
        jsonResponse = convertToJson(gpsevents)
        print(jsonResponse)
        return jsonResponse

    getFoxData()