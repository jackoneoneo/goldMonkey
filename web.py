from flask import Flask, request, render_template,redirect,url_for
import json
from plotyCellData import *
import time
from fileUtils import getFilesName,decompressionFile
import os

'''hdb下载存放的路径'''
baseFilePath = 'C:\\\\Users\\\\Administrator\\\\Downloads\\\\'
#baseFilePath = 'D:\\\\hdb\\\\'
filesubPath = '\\hdd\\db\\'
fileName = '' #日期目录db2018-11-3
dirFileName = '' #解压后的目录
dirPath = ''    #最内层的目录没有包含其他目录的目录
app = Flask(__name__,static_folder='',static_path='')

bcNum = 4  #bc的数量
'''使用ajax跨域的方式调用'''
@app.route('/find/<tarFileName>', methods=['GET', 'POST'])
def find(tarFileName):
        global dirFileName
        dirFileName = tarFileName+"_temp"
        global fileName
        fileName = os.path.splitext(tarFileName)[0]
        callback = request.args.get('callback')
        if os.path.isdir(baseFilePath + dirFileName + '\\' + filesubPath + '\\' + fileName):
            result = callback + "(" + json.dumps({"status":True}) + ")"
            return result
        else :
           result = callback + "(" + json.dumps({"status": False}) + ")"
           return result

@app.route('/home/<tarFileName>', methods=['GET', 'POST'])
def home(tarFileName):
        global dirFileName
        dirFileName = tarFileName+"_temp"
        global fileName
        fileName = os.path.splitext(tarFileName)[0]
        if os.path.isdir(baseFilePath + dirFileName + '\\' + filesubPath + '\\' + fileName):
            print('file is exsit,do not decompression.')
        else :
            decompressionFile(baseFilePath + tarFileName)
        return redirect(url_for('mainPage'))


@app.route('/mainPage', methods=['GET', 'POST'])
def mainPage():
        return render_template('chartDisplay.html')


@app.route('/bmulist/<bcdatabase>', methods=['GET', 'POST'])
def bmulist(bcdatabase):
        global dirPath
        return json.dumps(BmuNameList(dirPath+"\\"+bcdatabase))

@app.route('/dataChart/<databaseName>', methods=['GET', 'POST'])
def dataBCChart(databaseName):
    timeInteger = time.time()
    htmlName = str(timeInteger)+".html"
    '''此处路径需要修改'''
    createBCHtml(dirPath+'\\'+databaseName, htmlName,bcNum)
    return htmlName

@app.route('/bmuChart/<databaseName>/<BmuName>', methods=['GET', 'POST'])
def dataBmuhart(databaseName,BmuName):
    timeInteger = time.time()
    htmlName = str(timeInteger)+".html"
    '''此处路径需要修改'''
    createBmuHtml(dirPath+'\\'+databaseName, htmlName,BmuName,bcNum)
    return htmlName

@app.route('/html/<htmlName>', methods=['GET', 'POST'])
def d(htmlName):
    return render_template(htmlName)

@app.route('/databaseName', methods=['GET', 'POST'])
def databaseName():
    global dirPath
    dirPath = baseFilePath + dirFileName + '\\' + filesubPath + '\\' + fileName
    fileList = getFilesName(dirPath)
    global  bcNum
    bcNum = len(fileList)
    return json.dumps(fileList)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return "this is a test page"

if __name__ == '__main__':
    app.run()