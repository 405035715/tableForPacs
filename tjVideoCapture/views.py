from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
import tjVideoCapture
from django.core.urlresolvers import reverse
import pyodbc
from datetime import *
from django.http import JsonResponse
import json


#查询数据库
def selSql(selStr):
    sqlresult =[]
    connectStr = 'DRIVER={SQL Server};SERVER=192.168.1.6;PORT=1433;DATABASE=videocapture;UID=sa;PWD=easy'
    cnxn = pyodbc.connect(connectStr)
    cursor = cnxn.cursor()
    try:
        cursor.execute(selStr)
    except Exception as e:
        print(e)
    sum = 0
    while 1:
        row = cursor.fetchone()
        sum = sum + 1
        if not row:
            break
        sqlresult.append(list(row))
        #print(row)
    #print(sum)
    cnxn.close
    return sqlresult

def index(request):
    #统计表结构：【{name:,'checkcount'：,'feecount':,'examinebodypartySum:,'胶片':',detail:[{'mdlname':},,'checkcount'：,'feecount':,'examinebodypartySum:,'胶片'{}...]},】
    startDate = date.today().strftime('%Y-%m-%d')
    endDate = date.today().strftime('%Y-%m-%d')
    tongji = []     #检查部位的统计
    doctors = []    #检查医生
    bodyparts = []  #检查部位
    #tongjiall = []
    bodypart = ''
    # 查询检查医生
    selstr_doctors = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'sp_sel_Diagnostician\' ,\'\'  '
    doctors_tmp = selSql(selstr_doctors)
    for a in doctors_tmp:
        doctors.append(a[0])
    # 查询部位
    selstr_bodyparts = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'sp_sel_ExamineBody\' ,\'\'  '
    bodyparts_tmp = selSql(selstr_bodyparts)
    for a in bodyparts_tmp:
        bodyparts.append(a[1])
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        bodypart =  request.POST['bodypart']
        doctor = request.POST['doctor']
        if '全部' == bodypart:
            bodypart = ''
        if '全部' == doctor:
            doctor = ''

        #print(bodypart)

        #查询总表
        selstr_tongji = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'tj_bodypart_z\',\'@sbodypart=\'\'%s\'\',@odtRegisterBegin=\'\'%s\'\',@odtRegisterEnd=\'\'%s\'\', @diagnostician =\'\'%s\'\'  \'' %(bodypart,startDate,endDate,doctor)
        tongji = selSql(selstr_tongji)

    # for tj in tongji:
    #     t = []
    #     for tjDetail in tj:
    #         t.append(tjDetail)
    #     tongjiall.append(t)
        print(len(tongji))

    context = {
        'table_startDate':startDate,
        'table_endDate':endDate,
        'table_bodypart':bodypart,
        'table_tongji':tongji,
        'table_count':len(tongji),
        'bodyparts': bodyparts,
        'doctors': doctors
    }
    return  render(request,'tjVideoCapture/index.html',context)
