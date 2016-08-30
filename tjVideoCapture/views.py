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
    connectStr = 'DRIVER={SQL Server};SERVER=192.168.1.4;PORT=1433;DATABASE=videocapture;UID=sa;PWD=easy'
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
        print(row)
    #print(sum)
    cnxn.close
    return sqlresult



def index(request):
    #统计表结构：【{name:,'checkcount'：,'feecount':,'examinebodypartySum:,'胶片':',detail:[{'mdlname':},,'checkcount'：,'feecount':,'examinebodypartySum:,'胶片'{}...]},】
    startDate = date.today().strftime('%Y-%m-%d')
    endDate = date.today().strftime('%Y-%m-%d')
    tongji = []
    tongjiall = []
    bodypart = ''
    if request.method == 'POST':


        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        bodypart =  request.POST['bodypart']
        print(bodypart)
         #查询总表
        selstr_tongji = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'tj_bodypart_z\',\'@sbodypart=\'\'%s\'\',@odtRegisterBegin=\'\'%s\'\',@odtRegisterEnd=\'\'%s\'\'\'' %(bodypart,startDate,endDate)
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
    }
    return  render(request,'tjVideoCapture/index.html',context)
