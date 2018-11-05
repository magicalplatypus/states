import falcon
import msgpack

###accepts a JSON object in the form:
###	JSON = {"address":"300  Calla Lane"}

    
#import needed methods from driver class and database cursor
from .whatstateisit import execute as execute1, cur

#define the resources class the api will use
class appResource:
    #define behavior of api on get
	def on_get(self,req,resp):
		"""HANDLES put REQUESTS"""
		#returns state for particular address
		if req.get_param("address"): #if address has a value send address and cur to execute
			result =  execute1(cur,req.get_param("address"))
		else:
			result = 'no address entered' #if address is empty send error message
       #format and place result into the response     
		resp.data = msgpack.packb(result, use_bin_type = True)
        #set HTTP status code to 200
		resp.status = falcon.HTTP_200

    #ignore all other types of requests

#create api using falcon's constructor    
api = application = falcon.API()

#define app that waitress will be running
app = appResource()

#add resources to app
api.add_route('/states', app)