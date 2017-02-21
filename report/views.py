import datetime
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
import pyodbc


# 超声病人列表
def patientlistOfUS(request):
    # 查询条件
    name = ''
    startExamineTime = datetime.datetime.now() + datetime.timedelta(days = -1) #查询当天
    swhereTime = '' #时间查询条件
    if 'GET' == request.method:
        if request.GET.get('name'):
            name = request.GET.get('name')
        examineTime = request.GET.get('examinetime') #examinetime返回值：1，3，7，-1
        #print(examineTime)
        if examineTime in ['1','3','7']:
            if name == '请输入姓名' :
                name = ''
            startExamineTime = datetime.datetime.now() + datetime.timedelta(days= -int(examineTime))
        if examineTime == '-1':
            startExamineTime = startExamineTime + datetime.timedelta(days= -365*40)
            if name == '':  #用户在全部时间的情况下一定需要输入名字，如果不输入名字，就用-1代替
                pass
                #name = '请输入姓名'
    patintList = getPatientListOfUS(name, startExamineTime)
    context = {
         'patintlist': patintList,
         'name'      : name
    }
    return render(request, 'report/patientlistOfUS.html', context)


# 内镜病人列表
def patientlistOfENDO(request):
    # 查询条件
    name = ''
    startExamineTime = datetime.datetime.now() + datetime.timedelta(days = -1) #查询当天
    swhereTime = '' #时间查询条件
    if 'GET' == request.method:
        if request.GET.get('name'):
            name = request.GET.get('name')
        examineTime = request.GET.get('examinetime') #examinetime返回值：1，3，7，-1
        #print(examineTime)
        if examineTime in ['1','3','7']:
            startExamineTime = datetime.datetime.now() + datetime.timedelta(days= -int(examineTime))
        if examineTime == '-1':
            startExamineTime = startExamineTime + datetime.timedelta(days= -365*40)
    patintList = getPatientListOfENDO(name, startExamineTime)
    context = {
         'patintlist': patintList,
         'name'      : name
    }
    return render(request, 'report/patientlistOfENDO.html', context)


# 超声病人报告
def reportOfUS(request):
    patientid = request.GET.get('patientid')
    examinedate = request.GET.get('time')
    reportDic = getReportOfUS(patientid, examinedate)
    context = {
        'reportDic': reportDic,
    }
    return render(request, 'report/reportOfUS.html', context)

# 内镜报告
def reportOfENDO(request):
    patientid = request.GET.get('patientid')
    examinedate = request.GET.get('time')
    reportDic = getReportOfENDO(patientid, examinedate)
    context = {
        'reportDic': reportDic,
    }
    return render(request, 'report/reportOfENDO.html', context)

# 功能：查询超声的病人列表
# 查询条件：姓名：name；检查开始时间：startExamineTime
# 查询结果：paientid;name;sex;age;检查部位；检查时间；
def getPatientListOfUS(name,startExamineTime):
    swhereTime = ''  # 时间查询条件
    swhere = ''
    if '' != name:
        swhere = ' @PatName  = \'\'%s\'\' , ' % name  # 查询条件：姓名

    # 查询条件：时间：如果没有’开始的时间’，查询时不加查询时间的条件
    if startExamineTime:
        try:
            swhereTime = ' @ExamineTimeStart  =  \'\'%s\'\' ' % startExamineTime.strftime('%Y-%m-%d %H:%M:%S')
            #print(swhereTime)
        except:
            swhereTime = '' #转换datetime到str，如果出错，查询就不加时间条件
    if '' != swhereTime:
        swhere = swhere + swhereTime
    swhere = swhere
    reportsql = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'jd_PacsInfo\' , \' %s  \' ' % swhere
    print(reportsql)
    reportlist = selSql(reportsql, 'USDB')
    patintlist = []
    #截取列表，如果病人数量超过1000，只取前1000
    for a in reportlist:
        if len(a) > 15:
            reportDic = {}
            reportDic['patientid'] = a[0]  # patientid
            reportDic['name'] = a[1]  # name
            reportDic['sex'] = a[18]  # sex
            reportDic['age'] = a[2]  # age
            reportDic['bodypart'] = a[6]  # 检查部位
            reportDic['time'] = datetime.datetime.strftime(a[14], "%Y-%m-%d %H:%M:%S")  # 检查时间
            patintlist.append(reportDic)
    return patintlist


# 功能：查询内镜的病人列表
# 查询条件：姓名：name；检查开始时间：startExamineTime
# 查询结果：paientid;name;sex;age;检查部位；检查时间；
def getPatientListOfENDO(name,startExamineTime):
    swhereTime = ''  # 时间查询条件
    swhere = ''
    if '' != name:
        swhere = ' @PatName  = \'\'%s\'\' , ' % name  # 查询条件：姓名

    # 查询条件：时间：如果没有’开始的时间’，查询时不加查询时间的条件
    if startExamineTime:
        try:
            swhereTime = ' @ExamineTimeStart  =  \'\'%s\'\' ' % startExamineTime.strftime('%Y-%m-%d %H:%M:%S')
            #print(swhereTime)
        except:
            swhereTime = '' #转换datetime到str，如果出错，查询就不加时间条件
    if '' != swhereTime:
        swhere = swhere + swhereTime
    swhere = swhere
    reportsql = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'jd_PacsInfo\' , \' %s  \' ' % swhere
    print(reportsql)
    reportlist = selSql(reportsql, 'ENDODB')
    patintlist = []
    #截取列表，如果病人数量超过1000，只取前1000
    for a in reportlist:
        if len(a) > 15:
            reportDic = {}
            reportDic['patientid'] = a[0]  # patientid
            reportDic['name'] = a[1]  # name
            reportDic['sex'] = a[18]  # sex
            reportDic['age'] = a[2]  # age
            reportDic['bodypart'] = a[3]  # 检查部位
            reportDic['time'] = datetime.datetime.strftime(a[14], "%Y-%m-%d %H:%M:%S")  # 检查时间
            patintlist.append(reportDic)
    return patintlist

# 功能：查询病人的内镜报告
# 查询条件：patientid;检查时间：examinedate
# 查询结果：patientid;name;sex;age;检查部位:bodypart;所见：diagfind;印象conclusion；检查医生:doctor
def getReportOfENDO(patientid,examinedate):
    swhere = ' @PacsUid = \'\'%s\'\'   ' % (patientid)
    patientsql = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN   \'jd_PacsInfo\' ,\' %s  \' ' % swhere
    patientlist = selSql(patientsql, 'ENDODB')
    reportDic = {}
    if 1 == len(patientlist):  # 只有一条记录时
        patient = patientlist[0]
        #print(patient)
        reportDic['patientid'] = patient[0]  # patientid
        reportDic['name'] = patient[1]  # name
        reportDic['sex'] = patient[18]  # sex
        reportDic['age'] = patient[2]  # age
        reportDic['bodypart'] = patient[3]  # bodypart
        reportDic['time'] = datetime.datetime.strftime(patient[14], "%Y-%m-%d %H:%M:%S")  # 检查时间
        reportDic['diagfind'] = patient[10]  # diagfind 所见
        reportDic['conclusion'] = patient[11]  # conclusion 印象
        reportDic['doctor'] = patient[16]  # 检查医生
    return reportDic

# 功能：查询病人的超声报告
# 查询条件：patientid;检查时间：examinedate
# 查询结果：patientid;name;sex;age;检查部位:bodypart;所见：diagfind;印象conclusion；检查医生:doctor
def getReportOfUS(patientid,examinedate):
    swhere = ' @PacsUid = \'\'%s\'\'   ' % (patientid)
    patientsql = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN   \'jd_PacsInfo\' ,\' %s  \' ' % swhere
    patientlist = selSql(patientsql, 'USDB')
    reportDic = {}
    if 1 == len(patientlist):  # 只有一条记录时
        patient = patientlist[0]
        #print(patient)
        reportDic['patientid'] = patient[0]  # patientid
        reportDic['name'] = patient[1]  # name
        reportDic['sex'] = patient[18]  # sex
        reportDic['age'] = patient[2]  # age
        reportDic['bodypart'] = patient[6]  # bodypart
        reportDic['time'] = datetime.datetime.strftime(patient[14], "%Y-%m-%d %H:%M:%S")  # 检查时间
        reportDic['diagfind'] = patient[10]  # diagfind 所见
        reportDic['conclusion'] = patient[11]  # conclusion 印象
        reportDic['doctor'] = patient[16]  # 检查医生
    return reportDic

# 放射病人列表
def patientlistOfFSK(request):
    # 查询条件
    name = ''
    startExamineTime = datetime.datetime.now()+ datetime.timedelta(days = -1) #默认是当天
    swhereTime = '' #时间查询条件
    if 'GET' == request.method:
        if request.GET.get('name'):
            name = request.GET.get('name')
        examineTime = request.GET.get('examinetime') #examinetime返回值：1，3，7，30
        #print(examineTime)
        if examineTime in ['1','3','7']:
            if name == '请输入姓名':
                name = ''
            startExamineTime = startExamineTime + datetime.timedelta(days= -int(examineTime))
        if examineTime == '-1':
            startExamineTime = startExamineTime + datetime.timedelta(days= -365*40)
            if name == '':  #用户在全部时间的情况下一定需要输入名字，如果不输入名字，就用-1代替
               # name = '请输入姓名'
                pass
    patintList = getPatientListOfFSK(name, startExamineTime)
    context = {
         'patintlist': patintList,
         'name'      : name
    }
    return render(request, 'report/patientlistOfFSK.html', context)

# 功能：查询放射科的病人列表
# 查询条件：姓名：name；检查开始时间：startExamineTime
# 查询结果：paientid;name;sex;age;检查部位；检查时间；
def getPatientListOfFSK(name,startExamineTime):
    swhere = ''
    swhereTime = ''  # 时间查询条件
    if '' != name:
        swhere = ' @PatName = \'\'%s\'\' , ' %name  # 查询条件：姓名
    # 查询条件：时间：如果没有’开始的时间’，查询时不加查询时间的条件
    if startExamineTime:
        try:
            swhereTime = ' @ExamineTimeStart =  \'\'%s\'\' ' % startExamineTime.strftime('%Y-%m-%d %H:%M:%S')
            #print(swhereTime)
        except:
            swhereTime = '' #转换datetime到str，如果出错，查询就不加时间条件
    if '' != swhereTime:
        swhere = swhere + swhereTime
    reportsql = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'jd_PacsInfo\' ,\' %s  \' ' % swhere
    print(reportsql)
    reportlist = selSql(reportsql, 'FSKDB')
    #print(reportlist)
    patintlist = []
    #print(patintlist)
    for a in reportlist:
        if len(a) > 17:
            reportDic = {}
            reportDic['patientid'] = a[0]  # patientid
            reportDic['name'] = a[1]  # name
            reportDic['sex'] = a[18]  # sex
            reportDic['age'] = a[2]  # age
            reportDic['bodypart'] = a[6]  # 检查部位
            reportDic['time'] = datetime.datetime.strftime(a[14], "%Y-%m-%d %H:%M:%S")  # 检查时间
            reportDic['modality'] = a[7]
            patintlist.append(reportDic)
    return patintlist

# 放射科病人报告
def reportOfFSK(request):
    patientid = request.GET.get('patientid')
    reportDic = getReportOfFSK(patientid)
    context = {
        'reportDic': reportDic,
    }
    return render(request, 'report/reportOfFSK.html', context)

# 功能：查询病人的放射科报告
# 查询条件：patientid;
# 查询结果：patientid;name;sex;age;检查部位:bodypart;所见：diagfind;印象conclusion；检查医生:doctor
def getReportOfFSK(patientid):
    swhere = ' @PacsUid = \'\'%s\'\'   ' % (patientid)
    patientsql = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'jd_PacsInfo\' ,\' %s  \' ' % swhere
    patientlist = selSql(patientsql, 'FSKDB')
    reportDic = {}
    if 1 == len(patientlist):  # 只有一条记录时
        patient = patientlist[0]
        #print(patient)
        reportDic['patientid'] = patient[0]  # patientid
        reportDic['name'] = patient[1]  # name
        reportDic['sex'] = patient[18]  # sex
        reportDic['age'] = patient[2]  # age
        reportDic['bodypart'] = patient[6]  # bodypart
        reportDic['time'] = datetime.datetime.strftime(patient[14], "%Y-%m-%d %H:%M:%S")  # 报告时间
        reportDic['diagfind'] = patient[10]  # diagfind 所见
        reportDic['conclusion'] = patient[11]  # conclusion 印象
        reportDic['doctor'] = patient[16]  # 检查医生
        reportDic['modality'] = patient[7] #检查方式
    return reportDic


#查询数据库
def selSql(selStr, sqldbtype):
    sqlresult =[]
    connectStr = ''
    if 'USDB' == sqldbtype:
        connectStr = 'DRIVER={SQL Server};SERVER=127.0.0.1;PORT=1433;DATABASE=videocapture;UID=sa;PWD=easy'
    elif 'FSKDB' == sqldbtype:
        connectStr = 'DRIVER={SQL Server};SERVER=127.0.0.1;PORT=1433;DATABASE=espacs;UID=sa;PWD=easy'
    elif 'ENDODB' == sqldbtype:
        connectStr = 'DRIVER={SQL Server};SERVER=127.0.0.1;PORT=1433;DATABASE=gastroscope;UID=sa;PWD=easy'
    try:
        cnxn = pyodbc.connect(connectStr)
        cursor = cnxn.cursor()
        cursor.execute(selStr)
        while 1:
            row = cursor.fetchone()
            #sum = sum + 1
            if not row:
                break
            sqlresult.append(list(row))
            print(row)
        cnxn.close
    except Exception as e:
        print (e)
    return sqlresult
