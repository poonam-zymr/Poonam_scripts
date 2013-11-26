import requests
import json
import properties
import os
import time
import subprocess
import paramiko
import db
from apis import config_api,common_api
#import paramiko

def setpythonpath():
    cm_dir = properties.cm_path
    os.chdir(cm_dir)
    BASEDIR = os.getcwd()
    pythonpathfile = open("setpythonpath", "rb")
    for line in pythonpathfile:
        if "export PYTHONPATH" in line:
            newline = line.replace("$BASEDIR", BASEDIR)
    path = newline.split('=')
    envar = path[1]
    envar = envar.replace("\n", "")
    os.environ["PYTHONPATH"] = envar
    path = os.popen("echo $PYTHONPATH").read()
#This function does login and returns login session cookie
def login():
    loginrequest = properties.web_ui_baseurl+(common_api.login_api % (properties.username, properties.password))
    loginresponse = requests.get(loginrequest)
    #print loginresponse
    js = json.loads(loginresponse.text) 
    if 'id' in js['results'].keys():
        login_cookies = loginresponse.cookies
    else:
        login_cookies = None
    if login_cookies == None:
        raise AssertionError("Login is not successful.")
    else:
        print "Login is done successfully."
    return login_cookies

def start_runworkers(self):
    setpythonpath()
    time.sleep(5)
    workerstdoutfile = os.path.join(properties.outputFileLocation,
                                    "realap-runworkerstdout.txt")
    workerstderrfile = os.path.join(properties.outputFileLocation,
                                    "realap-runworkerstderr.txt")
    stdout = open(workerstdoutfile, "wb")
    stderr = open(workerstderrfile, "wb")
    # Navigate to the mom directory
    mom_dir = properties.mom_path
    os.chdir(mom_dir)
    print os.getcwd()
    print "Starting workers"
    # Start the runwokers process
    subprocess.Popen(['./runworkers'], stdout=stdout, stderr=stderr)
    time.sleep(120)

def start_apmanager(self):
    setpythonpath()
    time.sleep(5)
    apmanagerstdoutfile = os.path.join(properties.outputFileLocation,
                                       "realap-apmanagerstdout.txt")
    apmanagerstderrfile = os.path.join(properties.outputFileLocation,
                                       "realap-apmanagerstderr.txt")
    stdout = open(apmanagerstdoutfile, "wb")
    stderr = open(apmanagerstderrfile, "wb")

    # Navigate to the apmanager directory
    apmanager_dir = properties.apmanager_path
    os.chdir(apmanager_dir)
    print os.getcwd()
    print "Starting apmanager"
    apmanager = properties.apmanager
    # Start the apmanager process

    subprocess.Popen(['./apmctl.py', apmanager, 'start'], stdout=stdout,
                     stderr=stderr)
    time.sleep(120)

def real_ap_registration(real_ap):
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(properties.real_ap, username='root', password='password')
    apmanager_path = ("%s%s" % (properties.apmanager,
                                    properties.xmppdomain))
    print "Rebooting AP."
    reboot_command = "reboot"
    ssh.exec_command(reboot_command)
    time.sleep(180)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(properties.real_ap, username='root', password='password')
    services_stop = "monit stop xmpp_client"
    xmpp_client_filepath = os.path.join(properties.xmpp_client_path,
                                            "xmpp_client.conf")
    run_xmpp_client = "monit start xmpp_client"
    print ("Registering AP %s with apmanager %s" % (properties.real_ap, properties.apmanager))
    command = ("cd %s;%s;sed -i 's/XMPP_REGISTER=.*/XMPP_REGISTER='%s'/g' %s;%s" % (properties.xmpp_client_path, 
                    services_stop, apmanager_path, xmpp_client_filepath, run_xmpp_client))
    ssh.exec_command(command + ' > /dev/null 2>&1 &')
    time.sleep(60)
        # Verify if the ap entry is made in the database
    db.search_ap_in_new_ap_collection(properties.apjid)
    
def ap_onboarding(ap_jid, ap_serial_number):
    onboard_request = properties.web_ui_baseurl + (common_api.onboarding_api % (properties.customer_id, properties.location_id, ap_jid, ap_serial_number))
    login_cookie = login()
    onboard_response = requests.get(onboard_request, cookies=login_cookie)
    js = json.loads(onboard_response.text)
    if 'ap_id' in js['results'].keys():
        print ("AP is %s onboarded successfully!" % ap_jid)
    else:
        raise AssertionError("AP %s is not onboarded!" % ap_jid) 
