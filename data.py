
import copy;
data = {
        };
dataVAver = {
        };
dataIAver = {
        };
dataMonomerVol = {
        };




'''获取指定表下的单体电压'''
def MonomerVol(conn,tableName):  #指定表下的单体
    c = conn.cursor();
    tList = []; #某簇下单体电压的表名称
    originList = [];
    dataList = []; #存放单体电压的值

    cursor1 = c.execute("PRAGMA table_info("+tableName+")");
    for row in cursor1:
        if str(row[1]).find("CellVol") >= 0:
            tList.append(row[1]);
    sql = "select ";
    for i in tList:
        sql += i +",";
    sql += " date,time from "+tableName+";";
    cursor2 = c.execute(sql);
    x = [];
    overChargeData = [] #过压数据
    underChargeData = [] #欠压数据
    length = len(tList);
    for row in cursor2:   #把数据库中的信息保存在orginList中
        originList.append(row);
    for i in range(length):
        y = [];
        for row in originList:
            if 0 == i:
                x.append(row[length]+" "+row[length+1]);
                overChargeData.append(3.55)
                underChargeData.append(2.80)
            y.append(float(row[i]) / 1000);
        temp = copy.deepcopy(dataMonomerVol);
        temp['x'] = x;
        temp['y'] = y;
        dataList.append(temp);

    #过压数据
    overChargeVol = copy.deepcopy(dataMonomerVol)
    overChargeVol['x'] = x
    overChargeVol['y'] = overChargeData
    dataList.append(overChargeVol)

    # 欠压数据
    overChargeVol = copy.deepcopy(dataMonomerVol)
    overChargeVol['x'] = x
    overChargeVol['y'] = underChargeData
    dataList.append(overChargeVol);

    return dataList;

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
    X = []
    cursor = c.execute("SELECT date,time, VMax,VMin,VAvg,TMax,TMin,TMaxBmuId,TMinBmuId From bcmscommzone order by date;");
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
    dataList.append(voltageMax)
    dataList.append(voltageMin)
    dataList.append(voltageAvg)
    dataList.append(tempratureMax)
    dataList.append(tempratureMin)
    return dataList



def SOCAndBusVolandBusCurData(conn):
    listarr = [];
    c = conn.cursor();
    xSoc = [];
    ySoc = [];
    xV = [];
    yV = [];
    xI = [];
    yI = [];
    cursor = c.execute("select date,time,SOC,BusVol,BusCur from bcdmuzone;");
    for row in cursor:
        valuex = row[0] + " "+row[1];
        xSoc.append(valuex);
        xV.append(valuex);
        xI.append(valuex);
        # 簇SOCy轴数据
        valuey = float(row[2]) / 10;
        ySoc.append(valuey);
        # 簇电压y轴数据
        valueV = float(row[3]) /10;
        yV.append(valueV);
        #簇电流y轴数据
        valueI = row[4];
        yI.append(valueI);
    data['x']  = xSoc;
    data['y']  = ySoc;
    listarr.append(data);
    dataVAver['x'] = xV;
    dataVAver['y'] = yV;
    listarr.append(dataVAver);
    dataIAver['x'] = xI;
    dataIAver['y'] = yI;
    listarr.append(dataIAver);
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