
import sys
import psycopg2
import requests
import time
import random
import  json

def fetch_created_device_ids():
    dev_ids = []
    try:
        con = psycopg2.connect(database='test', user='postgres', password='postgres', host='localhost' , port=5432)
        cur = con.cursor()
        cur.execute("SELECT device_id from device where device_state='INIT'")
        #ver = cur.fetchall()
        print (cur)
        for record in cur:
            dev_ids.append(record[0])
            print (record[0])
    except psycopg2.DatabaseError as e :
        print ('Error %s' % e)

    return  dev_ids

def create_update_req():
    while (True):
        #sleep

        #1. Connect to db, find rows with STATE=CREATE
        dev_ids = fetch_created_device_ids()
        for dev in dev_ids:
            print ("Found device init")
            #2. Generate short/long transaction Ids
            ltrid = random.randint(1, 1000000000)
            strid = random.randint(1, 1000000000)

            #3. Invoke SCEF post API
            url = 'http://192.168.1.13:8080/3gpp_t8_nidd/v1/SmartStreetLighting@blr.com/configurations'
            data = """
            {
                "externalId": "StreetLight-BLR-12.9399178,77.6895246",
                "msisdn": "98873983003",
                "scsAsId": "SmartStreetLighting@blr.com",
                "ttrId": 111111111,
                "tltrId": 222222222,
                "duration": "34234327827584",
                "notificationDestination": "http://192.168.1.3:5000/v1/devices/notifDest/111111111",
                "pdnEstablishmentOption": "WAIT_FOR_UE" ,
                "reliableDataService": 1 ,
                "niddDownlinkDataTransfers": "48 65 6c 6c 6f 2c 20 77  6f 72 6c 64 21 0a 00 2e"
            }"""
            #format_args = [ltrid, strid]

            #json.loads(data)
            #formatted_data = {key: value.format(format_args) for key, value in data.items()}
            #print formatted_data

            try:
                response = requests.post(url, data=data, headers={"content-type":"application/json"})
                print (response)
            except requests.exceptions.ConnectionError:
                print ('Error, Connection Error')


            #4.
            print ("Sleeping while new device entries are created.....")
            time.sleep(10)


#if __name__ =="main":
print ("Running")
create_update_req()
