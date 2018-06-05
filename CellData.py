
import copy;
data = {
        };
dataVAver = {
        };
dataIAver = {
        };
dataMonomerVol = {
        }
dataClusterPower = {}

dataMonomerTemperature = {

}


'''获取指定表下的单体电压与温度'''
def MonomerVolAndTemperature(conn,tableName):  #指定表下的单体
    c = conn.cursor();
    vList = []; #某簇下单体电压的表名称
    tList = [] #某簇下单体温度
    originList = [];
    dataList = []; #存放单体电压的值
    temperatureList = [] #存放单体温度的值
    tVList = {} #存放所有单体温度与电压

    cursor1 = c.execute("PRAGMA table_info("+tableName+")");
    for row in cursor1:
        if str(row[1]).find("CellVol") >= 0:
            vList.append(row[1]);
        if str(row[1]).find("CellTemp") >= 0:
            tList.append(row[1])
    sql = "select ";

    for i in vList:
        sql += i +","

    for i in tList:
        sql += i +","

    sql += " date,time from "+tableName+";";
    cursor2 = c.execute(sql);
    x = [];

    overChargeData = [] #过压数据
    underChargeData = [] #欠压数据

    length = len(vList)
    print("vol:"+str(length))
    tLength = len(tList)
    print("temp:" + str(tLength))

    for row in cursor2:   #把数据库中的信息保存在orginList中
        originList.append(row)

    for i in range(length+tLength):
        y = []
        temperatureY = []
        for row in originList:
            if 0 == i:
                x.append(row[tLength + length]+" "+row[tLength + length +1])
                #print(row[tLength + length]+" "+row[tLength + length+1])
                overChargeData.append(3.55)
                underChargeData.append(2.80)
            if i < length:
                y.append(float(row[i]) / 1000); #添加单体电压
            else:
                temperatureY.append(float(row[i]) / 10) #添加单体温度

        if i < length:
            temp = copy.deepcopy(dataMonomerVol)
            temp['x'] = x;
            temp['y'] = y;
            dataList.append(temp)
        else:
            temperatureTemp = copy.deepcopy(dataMonomerTemperature)
            temperatureTemp['x'] = x
            temperatureTemp['y'] = temperatureY
            temperatureList.append(temperatureTemp)

    #过压数据
    overChargeVol = copy.deepcopy(dataMonomerVol)
    overChargeVol['x'] = x
    overChargeVol['y'] = overChargeData
    dataList.append(overChargeVol)

    # 欠压数据
    overChargeVol = copy.deepcopy(dataMonomerVol)
    overChargeVol['x'] = x
    overChargeVol['y'] = underChargeData

    dataList.append(overChargeVol)

    tVList["vols"] = dataList
    tVList["temps"] = temperatureList
    return tVList

'''获取指定数据库中bum的数量'''
def BmuNumber(conn):
    c = conn.cursor();
    cursor = c.execute("SELECT name FROM sqlite_master WHERE type='table';");
    number = 0;
    for row in cursor:
        if str(row).find("bcbmuzone") >= 0:
            number += 1;
    return number;

'''获取指定数据库中所有bmu的名称'''
def BmuList(conn):
    BmusName = []
    c = conn.cursor();
    cursor = c.execute("SELECT name FROM sqlite_master WHERE type='table';");
    number = 0;
    for row in cursor:
        if str(row).find("bcbmuzone") >= 0:
            BmusName.append(row)
    return BmusName

def d(conn):
    c = conn.cursor()
    cursor = c.execute("SELECT name FROM sqlite_master WHERE type='table';")

'''获取簇的最大单体电压、最小单体电压、平均单体电压、最小温度、最大温度'''
def temperatureAndVoltage(conn):
    c = conn.cursor()
    dataList = []
    voltageMaxY = []
    voltageMinY = []
    voltageAvgY = []
    tempratureMaxY = []
    tempratureMinY = []
    tempratureMaxBmuY = []
    tempratureMinBmuY = []
    X = []
    cursor = c.execute("SELECT date,time, VMax,VMin,VAvg,TMax,TMin,TMaxBmuInd,TMinBmuInd From bcmscommzone order by date;");
    for row in cursor:
        value =  row[0] + " "+row[1]
        X.append(value)
        valueVoltageMax = float(row[2]) / 1000
        voltageMaxY.append(valueVoltageMax)
        valueVoltageMin = float(row[3]) / 1000
        voltageMinY.append(valueVoltageMin)
        valueVoltageAvg = float(row[4]) / 1000
        voltageAvgY.append(valueVoltageAvg)
        ValueTempratureMax = float(row[5]) / 10
        tempratureMaxY.append(ValueTempratureMax)
        ValueTempratureMin = float(row[6]) / 10
        tempratureMinY.append(ValueTempratureMin)

        tempratureMaxBmuY.append(row[7])
        tempratureMinBmuY.append(row[8])

    voltageMax = {'name': '最大单体电压'}
    voltageMin = {'name': '最小单体电压'}
    voltageAvg = {'name': '平均单体电压'}
    tempratureMax = {'name': '最大温度'}
    tempratureMin = {'name': '最小温度'}
    tempratureMaxBmuId = {'name':'最大温度BmuId'}
    tempratureMinBmuId = {'name':'最小温度BmuId'}
    voltageMax['x'] = X
    voltageMax['y'] = voltageMaxY

    voltageMin['x'] = X
    voltageMin['y'] = voltageMinY

    voltageAvg['x'] = X
    voltageAvg['y'] = voltageAvgY

    tempratureMax['x'] = X
    tempratureMax['y'] = tempratureMaxY

    tempratureMin['x'] = X
    tempratureMin['y'] = tempratureMinY

    tempratureMaxBmuId['x'] = X
    tempratureMaxBmuId['y'] = tempratureMaxBmuY

    tempratureMinBmuId['x'] = X
    tempratureMinBmuId['y'] = tempratureMinBmuY

    dataList.append(voltageMax)
    dataList.append(voltageMin)
    dataList.append(voltageAvg)

    dataList.append(tempratureMax)
    dataList.append(tempratureMin)

    dataList.append(tempratureMaxBmuId)
    dataList.append(tempratureMinBmuId)

    return dataList


def getStackPower(conn):
    xPower = []
    ypower = []
    pass

def SOCAndBusVolandBusCurDataAndPower(conn,bcNum):
    listarr = [];
    c = conn.cursor();
    xSoc = [];
    ySoc = [];
    xV = [];
    yV = [];
    xPower = []
    ypower = []
    xI = [];
    yI = [];
    cursor = c.execute("select date,time,SOC,BusVol,BusCur,power from bcdmuzone;");
    for row in cursor:
        valuex = row[0] + " "+row[1];
        xSoc.append(valuex);
        xV.append(valuex);
        xI.append(valuex);
        xPower.append(valuex)
        # 簇SOCy轴数据
        valuey = float(row[2]) / 10;
        ySoc.append(valuey);
        # 簇电压y轴数据
        valueV = float(row[3]) /10;
        yV.append(valueV);
        #簇电流y轴数据
        valueI = row[4]
        yI.append(valueI)
        #簇功率
        valueP =  (float(row[5]) / 10000) * bcNum
        ypower.append(valueP)

    data['x']  = xSoc
    data['y']  = ySoc
    listarr.append(data)

    dataVAver['x'] = xV
    dataVAver['y'] = yV
    listarr.append(dataVAver)

    dataIAver['x'] = xI
    dataIAver['y'] = yI
    listarr.append(dataIAver)

    dataClusterPower['x'] = xPower
    dataClusterPower['y'] = ypower
    listarr.append(dataClusterPower)
    return listarr;

'''
def getAllData():
    data = []
    util = Dbutils("000203004bcms1.db")
    conn = util.connectDb()
    count = BmuNumber(conn)
    for i in range(count):
        data += MonomerVol(conn,"bcbmuzone"+str(i+1),i+1);
    data += SOCAndBusVolandBusCurData(conn);
    conn.close();
    return data;




def createHtml(htmlPath):
    f = codecs.open(htmlPath,"w","UTF-8")
    fheader = codecs.open("./templates/header.txt", "r", "UTF-8")
    f.write(fheader.read())
    f.write("var data = " + json.dumps(getAllData()))
    ftemp = codecs.open("./js/temp.txt","r","UTF-8")
    f.write(ftemp.read())
    f.write("</script>")
    ftemp.close()
    f.close()
print(data['name'])
'''