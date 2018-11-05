#python version 3.7.1
#postgresql version 11

The api accepts a JSON object in the form:
	JSON = {"address":"300  Calla Lane"}

inside main folder of project enter:
	pip install virtaulenv
	virtualenv venv
	cd venv/scripts
		activate.bat
	cd ../..
	pip install falcon
	pip install psycopg2
	pip install requests
	pip install waitress
	pip install msgpack-python

To connect to your local database:
	in whatstateisit.py:	
		replace database with database name
		replace userVal with db username
		replace passwordVal with db password
   		replace keyVal with your google api key
		replace schemaNVal with the name of schema used in your db
		replace tableNVal with  name of table used in your db

to start server:
	waitress-server --port 8000 states.app:api

test in postman with:
	get request
	to: localhost:8000/states
	params: key: "address"
		value: theAddress
		
