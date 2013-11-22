import requests
import json     
import properties
import utils
import db
from time import gmtime, strftime
from apis import config_api,common_api

def get_config_list(cookies):
    configrequest = properties.web_ui_baseurl + (config_api.config_list_api % properties.customer_id)
    config_response = requests.get(configrequest,cookies=cookies)
    js = json.loads(config_response.text)
    return js

def get_customer_list(cookies):
    customer_request = properties.web_ui_baseurl + common_api.customers_api
    customer_response = requests.get(customer_request,cookies=cookies)
    js2 = json.loads(customer_response.text)
    return js2

def create_config_blob(config_name):
    login_cookie = utils.login()
    #Use these asserts in the login function-done
    js = get_config_list(login_cookie)
    for i in range(len(js['results'])):    
        ourResult = js['results'][i]['config_name']
        #Shrushti - No need to check for config id or if you want to put this check assert if the config is present
        #and stop the test there with a message "Config $config-name already exists!"
        if config_name in ourResult:
            raise AssertionError("Config blob %s already exists!" % config_name)
        ##if config blob is already present then create new blob with timestamp
            timestamp=strftime("_%Y_%m_%d_%H_%M_%S", gmtime())
            config_name=config_name+timestamp
            createconfig_request = properties.web_ui_baseurl + (config_api.create_config_api % config_name)
        else:
            #Shrushti- Create a config with a name such that AcceleraConfig_(timestamp)
            #Shrushti - No need to pass config id in the request
            createconfig_request = properties.web_ui_baseurl + (config_api.create_config_api % config_name)
    createconfig_response = requests.get(createconfig_request,cookies=login_cookie)
    js1 = json.loads(createconfig_response.text)
    if 'Configuration Updated in DB!' in js1['results']['message'] or 'Configuration Saved in DB!' in js1['results']['message']:
        #While printing always print the variable so it is easier to debug scripts
        print ("Configuration blob %s is added in database successfully." % (config_name))    
    else:
        raise AssertionError("Configuration blob %s is not created and added in database." % (config_name))

##This function returns config id for given configuration blob
def retrieve_config_id(config_name):
    login_cookie = utils.login()
    js3 = get_config_list(login_cookie)
    config_id=None
    for i in range(len(js3['results'])):    
        ourResult = js3['results'][i]['config_name']
        if config_name == ourResult:
            config_id = js3['results'][i]['id']
    if config_id == None:
        raise AssertionError("Configuration blob %s is not exist" % config_name)
    return config_id

#This function pushes config to customer
def push_config_to_customer():
    global customer_id, config_id
    config_id=None
    login_cookie = utils.login()
    js2 = get_customer_list(login_cookie)
    for i in range(len(js2['results'])):    
        ourResult = js2['results'][i]['name']
        if properties.customer_name == ourResult:
            customer_id = js2['results'][i]['id']
            js = get_config_list(login_cookie)
            #print js
            print len(js['results'])
            for i in range(len(js['results'])):    
                ourResult = js['results']['config_name']
                if properties.configuration_name in ourResult:
                    config_id = js['results'][i]['id']
                    print config_id
                    default_config_request = properties.web_ui_baseurl + (config_api.push_config_to_customer_api % (customer_id,config_id))
                    config_update_response = requests.get(default_config_request, cookies=login_cookie)
                    js3 = json.loads(config_update_response.text)
                    if "Default Configuration of Customer updated" in js3['results']['message']:
                        print ("Default config %s is applied to customer %s successfully." % (properties.configuration_name, properties.customer_name))
                    else:
                        raise AssertionError("Default config %s is not applied to customer %s." % (properties.configuration_name, properties.customer_name))

def push_config_to_ap(ap_id, ap_jid):
    login_cookie = utils.login()
    #SHrushti - Use these asserts in the login function-done
    #Shrushti - Rename variable ap_name to ap_jid in the function-done
    config_id = retrieve_config_id(properties.configuration_name)
    if config_id != None:
        push_config_request = properties.web_ui_baseurl + (config_api.push_config_to_AP_api % (ap_id, config_id, properties.customer_id))
        push_config_response = requests.get(push_config_request, cookies=login_cookie)
        js3 = json.loads(push_config_response.text)
        if "Configuration template change initiated" in js3['results']['message']:
                #Shrushti - Use variable names in print statements-done
                print ("Default config %s is applied to AP %s successfully." % (properties.configuration_name,ap_jid))
        else:
            raise AssertionError("Default config %s is not applied to AP %s." % (properties.configuration_name,ap_jid))
    return config_id
                #Shrushti - Add assertion error as above function-done
                #This block checks whether config_id field points to correct config blob in database.-done
                #Shrushti - Create a new function to verify pushed config in db-done