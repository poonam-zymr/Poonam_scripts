import os
import subprocess
import time
import properties
import paramiko
from utils import utils,db
import sys
import pymongo
import re


class TestValidRealAPRegistration:

    def test_runworkers(self):
        utils.setpythonpath()
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

    def test_start_apmanager(self):
        utils.setpythonpath()
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
        subprocess.Popen(['./apmctl.py', apmanager, 'start'], stdout=stdout,
                         stderr=stderr)
        time.sleep(120)

    def test_real_ap_registration(self):

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

obj = TestValidRealAPRegistration()
obj.test_runworkers()
obj.test_start_apmanager()
obj.test_real_ap_registration()
