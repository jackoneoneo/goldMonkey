import sqlite3;


class Dbutils:
    def __init__(self,sqliteDbName):
        self.dbName = sqliteDbName;
# 连接数据sqlite db ,返回连接的结果，使用后记得关闭这个返回对象
    def connectDb(self):
        conn = sqlite3.connect(self.dbName);
        return conn;



