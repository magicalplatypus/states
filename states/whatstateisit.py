# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:27:30 2018

@author: Patrick
"""


import psycopg2
import requests
#import json


###VERSIONS###
#postgresQL 11
#compatible with: python 3.7
#falcon version 1.4.1

###database connection specifications###
#host will always be localhost#
#host = "localhost"
database = "databaseVal"
user = "userVal"
password = "passwordVal"
#change schemaN and tableN to match where local DB stores geometry information about states
schemaN = 'schemaNVal'
tableN = 'tableNVal'    
#enter key for google api
key = 'keyVal'


# call 1st to start database connection
# returns a cursor object to access db
#takes a connection as paramter
def connectDB(database,user,password):
    
    
    try:
        #connect to server
        conn = psycopg2.connect(dbname = database, user = user, password = password)
        print ('DB Connection Created')
        #create cursor to keep track of db connection
        cur = conn.cursor()
        return cur
        #print error message if an error occurs
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
 

    
#closes database connection and cursor    
#takes cursor and connection as input   
def closeDB(cur):
    cur.close()
    print ('DB Connection Closed')
    
    
    
#find latitude and longitude of specific address entered
#takes google API key and address as parameter
def getLatLong(address, key):
    #define url and parameters for json request
    GOOGLE_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    parameters = {
            'address': address,
            'key': key
            }

    #create and execute json request
    req = requests.get(GOOGLE_API_URL, params=parameters)
    results = req.json()
    
    #get status for error checking
    status = results['status']
    
    #check to see if google api failed
    if status == "ZERO_RESULTS" :
        print ("google api failed")
        return "address was invalid", "address was invalid"
    
    #if google api returns OK fill lat and long with their values
    if status == "OK" :
        result = results['results'][0]
    lat = result['geometry']['location']['lat']
    lng = result['geometry']['location']['lng']
    return lat,lng



#format query for postgres and return state
#takes a cursor, geoLoc dictionary, the db schema name as a string,
# and the table name as string  object as parameters
def getState(cur,geoLoc,schemaN,tableN):
      
    #format query 
    query1 = "SELECT name FROM \""+ schemaN +"\"."+ tableN + " WHERE ST_Contains(geom, ST_Transform(ST_GeometryFromText(\'POINT("
    query2 = ")\',4269), 4269));"
    query = query1 + str(geoLoc['lng']) +' ' + str(geoLoc['lat']) + query2
    #Make queryto postGis postgreSQL database and get answer 
    cur.execute(query)
    state = cur.fetchone()
    
    #remove formatting from text and return state
    return state[0]



#returns the state from address inputted.
#takes in cursor and address from api
def execute(cur, address):
	
     #get lat long from address through google api
     lat, lng = getLatLong(address,key)
     #check if error message was placed in Lat
     if lat != "address was invalid" :
         #if lat lng returned correctly query database for state
         state = getState(cur, lat, lng , schemaN, tableN)
         #check if db returns none for no results
         if state != None :
             #if results returned print state to console and return state as a string to user
             print (state)
             return str(state[0])
         #message for when query fails: address outside of US
         print ("Address entered was outside of the United States.")
         return "Address entered was  outside of the Unites States. Please try a different address."
     #message for when google api fails
     print ("Address was invalid")
     return "Address entered was invalid. Please try a different address."




#create db connection 
cur = connectDB(database,user,password)


    



