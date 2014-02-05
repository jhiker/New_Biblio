import cgi
import datetime, json
import urllib

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users
from webapp2_extras import sessions

import jinja2
from jinja2 import Environment, PackageLoader
import os

from pages import *
from models import *

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()



    institutions= ['Publisher','Lending Library (Public)','Lending Library (Private)','Bookdealer','Private Collection','Museum Collection','Prison Camp','Displaced Persons Camp','Research or University Library','Other']
    fates=['Dissolved', 'Liquidated', 'Sold at Auction', 'Still Active' , 'Unknown']
 


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/enterprovdata', ProvData),
                               ('/enterbookdata', BookData),
                               ('/provenance', Provenance),
                               ('/place', DisplayInst),
                               ('/provenanceDel', DeleteProv),
                               ('/provpoints', ProvPoint),
                               ('/img', Image),
                               ('/book', BkDisplay),
                               ('/error', Errorclass),
                               ('/finalBook', finalBook),
                               ('/enterbookdata', BookData)],
                              config=config,
                              debug=True)
