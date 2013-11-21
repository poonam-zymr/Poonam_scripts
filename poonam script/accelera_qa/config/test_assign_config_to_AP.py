from apis import config_api
from utils import utils,config_utils,results,db
import pymongo
import unittest
import properties
import requests
import json
import time
#from test_create_config import TestCreateConfig
    
class TestPushConfigToAP(unittest.TestCase):
    #Shrushti - create a setup function to runworkers, apmanager and xmpp client for AP
    def setUp(self):
        pass
        utils.start_runworkers()
        utils.start_apmanager()
        utils.real_ap_registration(properties.real_ap)
    def test_assign_config_to_ap(self):
        ap_jid = properties.apjid
        ap_id=db.search_ap_in_new_ap_collection(ap_jid)   
        utils.ap_onboarding(ap_id, ap_jid)
        db.search_ap_in_ap_collection
        config_id=config_utils.push_config_to_ap()
        db.verify_ap_running_config_id(ap_jid, config_id)
        #Shrushtu - As above create a seperate function to check if running config id is updated in mongo db with the created config
def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPushConfigToAP))
    print suite
    print __file__
    results.run(suite, __file__) 

                
                 
