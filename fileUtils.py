import tarfile;
import os;

'''解压指定的文件'''
def decompressionFile(fileName):
    tar = tarfile.open(fileName)
    names = tar.getnames()
    if os.path.isdir(fileName + "_temp"):
        dirPath = fileName + "_temp"
        dirPath = dirPath.replace("\\", "\\\\")
        os.system("rmdir /s /q "+dirPath)
    os.mkdir(fileName + "_temp")
    # 因为解压后是很多文件，预先建立同名目录
    for name in names:
       tar.extract(name, fileName + "_temp/")
    tar.close()


def getFilesName(dirPath):
    fileList = []
    fileTuple = os.walk(dirPath)
    for  root, dirs, files in fileTuple:
        for file in files:
            if os.path.splitext(file)[1] == '.db' and os.path.splitext(file)[0].find('bcms') >=0:
                #print(os.path.join(root,file))
                fileList.append(file)
    return fileList