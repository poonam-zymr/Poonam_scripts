import requests
import json
import properties
import config_utils
import pymongo

#This function returns specific collection data
def retrieve_collection(collection_name):
    mongo_db_ip = properties.mongo_ip
    connection = pymongo.MongoClient(mongo_db_ip)
    db_name = properties.db_to_be_used
    mongo_db = connection[db_name]
    mongo_collection = mongo_db[collection_name]
    connection.disconnect()
    return mongo_collection
    
#This function verifies whether default config is applied to customer
def verify_customer_default_id(config_id, customer_id):
    mongo_collection = retrieve_collection(properties.customer_collection_name)
    mongo_document = mongo_collection.find_one({"name" : properties.customer_name},{"default_config_id" : 1})
    if str(mongo_document['_id']) == str(customer_id):
        if not str(mongo_document['default_config_id']) == str(config_id):
            raise AssertionError("Default config %s is not assigned to customer %s." % (config_id,properties.customer_name))
        else:
            print ("Default config %s is assigned to customer %s." (config_id,properties.customer_name))

#This function checks whether AP gets added in new_ap collection after registration
def search_ap_in_new_ap_collection(ap_jid):
    # mongo_ap_collection = db.retrieve_collection(properties.ap_collection_name)
    mongo_newap_collection = retrieve_collection(properties.new_ap_collection_name)
    mongo_newap_document = mongo_newap_collection.find_one({"apid" : ap_jid},{"_id" : 1})
    ap_id = str(mongo_newap_document['_id'])
    if mongo_newap_document != None:
        print ("AP %s is registered successfully and added in new_ap collection." % ap_jid)
    else:
        raise AssertionError("AP %s is not added in new_ap collection." % ap_jid) 
    return ap_id

#This function checks whether AP gets added in ap collection after onboadring
def search_ap_in_ap_collection(ap_jid):
    mongo_ap_collection=retrieve_collection(properties.ap_collection_name)
    mongo_ap_document = mongo_ap_collection.find_one({"apid" : ap_jid},{"ap_name" : 1})
    ap_name = str(mongo_ap_document['ap_name'])
    if ap_name == properties.apjid:
        print ("AP %s is found in ap collection." % ap_jid)
    else:
        raise AssertionError("AP %s is not found in ap collection." % ap_jid)

def verify_ap_running_config_id(ap_jid, config_id):
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    mongo_ap_document = mongo_ap_collection.find_one({"apid" : ap_jid})
    running_config_id = str(mongo_ap_document['running_config_id'])
    if running_config_id == str(config_id):
        print ("Config %s is pushed to AP %s successfully." % (config_id,ap_jid))
    else:
        raise AssertionError("Config %s is not pushed to AP %s." % (config_id,ap_jid))
    

    
    
    