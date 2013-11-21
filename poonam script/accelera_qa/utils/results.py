import os
import HTMLTestRunner
import platform
import codecs
import glob
import properties
from time import gmtime, strftime

def run(suite, filepath):
    resultpath = properties.Results
    filePath, fileExtension = os.path.splitext(filepath)
    filename = os.path.split(filePath)
    filename1 = os.path.split(filename[0])
    resultdir = os.path.join(resultpath, 'html_result', filename1[1])
    suitename = os.path.split(filename[0])
    if not os.path.exists(resultdir):
        os.makedirs(resultdir)
    os.chdir(resultdir)
    cnt=0
    for files in glob.glob("*.html"):
        if filename[1] in files:
            cnt = cnt+1
    if cnt != 0:
        ext = ("_%s.html" % cnt)
    else:
        ext = ".html"
    resultfile = os.path.join(resultdir, filename[1] + ext)
    testcasename = filename[1]
    with open(resultfile, "wb") as f:
        runner = HTMLTestRunner.HTMLTestRunner(
                    stream = f,
                    verbosity=2,
                    title='Test execution report',
                    description='Result of tests'
                    )
        runner.run(suite)
    f.close()
    write_index(resultfile, suitename[1], testcasename)
    os.chdir(filename[0])

def write_index(resultfile, suitename, testcasename):
    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"> 
    <html>
    <head> 
    <meta content="text/html; charset=ISO-8859-1" 
    http-equiv="content-type"> 
    <title>Links to result files</title> 
    </head>
    <h2> Index to Result Files</h2>
    <p><br><b>      Test Suite:-&nbsp;&nbsp;&nbsp;%s</b></br>
    <br>Execution Summary:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</br>
    Test case:-&nbsp;&nbsp;&nbsp;<a href='%s'><b style="background-color:%s;">%s</b></a><b>&nbsp;&nbsp;Count:- %s&nbsp;&nbsp;</b><b style="background-color:%s;">Pass:- %s&nbsp;&nbsp;</b><b style="background-color:%s;">Fail:- %s&nbsp;&nbsp;</b><b style="background-color:%s;">Error:- %s</b>
    </p>
    </html>
    '''
    contents1 = '''
    <p>Execution Summary:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s
    <br>Test case:-&nbsp;&nbsp;&nbsp;<a href='%s'><b style="background-color:%s;">%s</b></a><b>&nbsp;&nbsp;Count:- %s&nbsp;&nbsp;</b><b style="background-color:%s;">Pass:- %s&nbsp;&nbsp;</b><b style="background-color:%s;">Fail:- %s&nbsp;&nbsp;</b><b style="background-color:%s;">Error:- %s</b></br>
    </p>
    '''
    
    indexfilepath = os.path.split(resultfile)
    indexfilepath1 = os.path.join(indexfilepath[0], "index.html")
    htmlfile = indexfilepath[1].split('.') 
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    fh = None
    linecnt = None
    lineend = None
    array = []
    passtag = 'white'
    failtag = 'white'
    errortag = 'white'
    tag = 'green'
    fh1 = open(resultfile, "rb")
    for num,line in enumerate(fh1):
        if "id='total_row'" in line:
            linecnt = num + 2
            lineend = linecnt+4
        if num == linecnt and num < lineend:
            linecnt = linecnt + 1
            array.append(line)
        elif num == lineend:
            break
    for num, each in enumerate(array):
        each1 = each.replace("<" and ">" and "=" and "td" and "/", "")
        each1 = each1.replace("<td>","")
        if num == 0:
            count = int(each1)
        elif num == 1:
            passcnt = int(each1)
            if passcnt > 0:
                passtag = 'green'
        elif num == 2:
            failcnt = int(each1)
            if failcnt > 0:
                failtag = 'red'
                tag = 'red'
        elif num == 3:
            errorcnt = int(each1)
            if errorcnt > 0:
                errortag = 'purple'
                tag = 'red'
    if os.path.exists(indexfilepath1):
        fh = codecs.open(indexfilepath1, "a+")
        fh.write(contents1 % (time, indexfilepath[1], tag, testcasename, count, passtag, passcnt, failtag, failcnt, errortag, errorcnt))
    else:
        fh = codecs.open(indexfilepath1, "w+")
        fh.write(contents % (suitename, time, indexfilepath[1], tag, testcasename, count, passtag, passcnt, failtag, failcnt, errortag, errorcnt))

def write_main_index(resultlocation):
    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"> 
    <html>
    <head> 
    <meta content="text/html; charset=ISO-8859-1" 
    http-equiv="content-type"> 
    <title>Main Index File</title> 
    </head>
    <h2> Main Index</h2>
    <p><b> Test Suite: %s </b>
    <br>Result Index File: <a href='%s'>Index</a><br>
    Coverage Index File: <a href='%s'>Index</a>
    </p>
    </html>
    '''
    contents1 ='''
    <p><b> Test Suite: %s </b>
    <br>Result Index File: <a href='%s'>Index</a></br>
    Coverage Index File: <a href='%s'>Index</a>
    </p>
    '''

    os.chdir(resultlocation)
    mainindexfilepath = os.path.join(resultlocation, 'Main_Index.html')
    if os.path.exists(mainindexfilepath):
        os.remove(mainindexfilepath)
    suitename = None
    suitename1 = None
    fh = None
    coverageindexfiles = []
    resultindexfiles = []
    for dirn,dir,files in os.walk(resultlocation):
        for file in files:
            if 'index.html' in file:
                if 'html_coverage_result' in dirn:
                    dir1 = os.path.split(dirn)
                    htmlindexfile = os.path.join(dirn,file)
                    coverageindexfiles.append(htmlindexfile)
                elif 'html_result' in dirn:
                    dir2 = os.path.split(dirn)
                    suitename1 = dir2[1]
                    resultindexfile = os.path.join(dirn,file)
                    resultindexfiles.append(resultindexfile)
    for num,each in enumerate(coverageindexfiles):
        suitename = os.path.split(os.path.dirname(each))
        for num1,each1 in enumerate(resultindexfiles):
            suitename1 = os.path.split(os.path.dirname(each))
            if num == num1:
                if suitename != None and suitename1 != None:
                    if suitename[1] ==  suitename1[1]:
                        coverageindexfile = os.path.relpath(each, resultlocation)
                        resultindexfile = os.path.relpath(each1, resultlocation)
                        if os.path.exists(mainindexfilepath):
                            fh = codecs.open(mainindexfilepath, "a+")
                            fh.write(contents1 % (suitename[1], resultindexfile, coverageindexfile))
                        else:
                            fh = codecs.open(mainindexfilepath, "w+")
                            fh.write(contents % (suitename[1], resultindexfile, coverageindexfile))  
                            


    
