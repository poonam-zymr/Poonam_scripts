import os
import HTMLTestRunner
import platform
import codecs
import glob
from time import gmtime, strftime

def run(suite, filepath):
    filePath, fileExtension = os.path.splitext(filepath)
    filename = os.path.split(filePath)
    resultdir = os.path.join(filename[0], 'Results')
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
    print resultfile
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
    
                            


    
