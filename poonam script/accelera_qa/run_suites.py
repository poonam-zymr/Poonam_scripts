import unittest
import sys
import os
import properties
import shutil
from utils import results

def run_suite():
    resultdir = properties.Results 
    curdir = os.getcwd()
    suitefile = os.path.join(curdir, 'suite.conf')
    suites = []
    if os.path.exists(suitefile):
        fh = open(suitefile, 'r')
        for line in fh:
            if " " not in line and "#" not in line:
                print line
                line = line.replace("\n", "")
                line = line.replace("\t", "")
                line = line.replace("\r", "")
                line = line.replace(" ", "")
                line = line.lower()
                suites.append(line)
    configfiles = [0]*(len(suites))
    for dirname,dirs,files in os.walk(curdir):
        for file in files:
            if 'config_current.ini' in file:
                suitepath = os.path.split(dirname)
                suitename = suitepath[1]   
                suitename = suitename.lower()
                if suitename in suites:
                    index = suites.index(suitename)
                    configpath = os.path.join(dirname,file)
                    configfiles.pop(index)
                    configfiles.insert(index, configpath)
    resultlocation = os.path.join(resultdir,'html_result')
    coverageresults = os.path.join(resultdir,'html_coverage_result')
    if os.path.exists(resultlocation):
        shutil.rmtree(resultlocation, ignore_errors='true')
    if os.path.exists(coverageresults):
        shutil.rmtree(coverageresults, ignore_errors='true')
    for each in configfiles:
        sourcedir = os.path.dirname(each)
        os.chdir(sourcedir)
        sourcedir1 = os.path.split(sourcedir)
        sourcedir = os.path.join(os.path.dirname(each),"htmlcov")
        destidir = os.path.join(coverageresults,sourcedir1[1])
        command = ("nosetests -c %s" % each)
        os.system(command)
        if os.path.exists(sourcedir):
            shutil.move(sourcedir,destidir)
    os.chdir(curdir)
    results.write_main_index(resultdir)
