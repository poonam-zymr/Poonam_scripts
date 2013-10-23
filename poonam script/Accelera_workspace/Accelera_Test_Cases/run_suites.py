import unittest
import sys
import os
import properties
import shutil
import main_index

def run_suite(resultdir):
    curdir = os.getcwd()
    suitefile = os.path.join(curdir, 'suite.conf')
    suites = []
    if os.path.exists(suitefile):
        fh = open(suitefile, 'r')
        for line in fh:
            if 'suite_' in line:
                line = line.replace("\n", "")
                line = line.replace("\t", "")
                line = line.replace("\r", "")
                line = line.lower()
                suites.append(line)
    configfiles = [0]*len(suites)
    for dirname,dir,files in os.walk(curdir):
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
    parentdir = os.path.split(curdir)
    resultlocation = os.path.join(resultdir,parentdir[1])
    if os.path.exists(resultlocation):
        shutil.rmtree(resultlocation, ignore_errors='true')
    for each in configfiles:
        sourcedir = os.path.dirname(each)
        if os.path.exists(os.path.join(sourcedir, "Results")):
            shutil.rmtree(os.path.join(sourcedir, "Results"), ignore_errors='true')
        os.chdir(sourcedir)
        command = ("nosetests -c %s" % each)
        os.system(command)
        suitename = os.path.split(sourcedir)
        destidir = os.path.join(resultlocation, suitename[1])
        shutil.copytree(sourcedir, destidir, symlinks=False, ignore=shutil.ignore_patterns('*.py', '*.ini', '*.pyc', '*.coverage'))
    main_index.write_main_index(resultlocation)
    os.chdir(curdir)

