from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
import tablespacs
from django.core.urlresolvers import reverse
import pyodbc
from datetime import *
from django.http import JsonResponse
import json

#查询数据库
def selSql(selStr):
    sqlresult =[]
    connectStr = 'DRIVER={SQL Server};SERVER=192.168.1.6;PORT=1433;DATABASE=espacs;UID=sa;PWD=easy'
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
#插入数据库:espacs
def insertSql(insertStr):
    connectStr = 'DRIVER={SQL Server};SERVER=192.168.1.6;PORT=1433;DATABASE=espacs;UID=sa;PWD=easy'
    cnxn = pyodbc.connect(connectStr)
    cursor = cnxn.cursor()
    try:
        cursor.execute(insertStr)
    except Exception as e:
        print(e)
    cnxn.commit()
    cnxn.close


def index(request):
    #统计表结构：【{name:,'checkcount'：,'feecount':,'examinebodypartySum:,'胶片':',detail:[{'mdlname':},,'checkcount'：,'feecount':,'examinebodypartySum:,'胶片'{}...]},】
    startDate = date.today().strftime('%Y-%m-%d')
    endDate = date.today().strftime('%Y-%m-%d')
    tongjiall = [] #['tongji:[('金国清', 5, 0.0, 5, 0)],'tongjiDetail':[[('陈俊杰', 'CT', 1, 0.0, 1, 0)],]']
    tongjicount = [0,0,0]#[检查人次,费用，部位，胶片]
    tongji_film_count = '' #总的胶片量
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        #查询总表
        selstr_tongji = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'tj_getClinicalDoctor_bodypart_fee\',\'@sModality=0, @odtRegisterBegin=\'\'%s\'\',@odtRegisterEnd=\'\'%s\'\'\'' %(startDate,endDate)
        tongji = selSql(selstr_tongji)
        #胶片统计-分送检医生
        selstr_tongji_films = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'tj_getClinicalDoctor_bodypart_film\',\'@odtRegisterBegin=\'\'%s\'\',@odtRegisterEnd=\'\'%s\'\'\'' %(startDate,endDate)
        tongji_films = selSql(selstr_tongji_films)
        tempclinicaldoctors = []
        tongji_film = [] # [{name:,film:[{SIZE:,count:},] },]
        for row in tongji_films:
            #print(row)
            #row:['俞雪华', 'CT', '14INX17IN', 2]
            if row[0] not in tempclinicaldoctors:
                tempclinicaldoctors.append(row[0])
                b = {}
                b['name']= row[0]
                c =[]
                d = {}
                d['size']= row[2]
                d['count']= row[3]
                c.append(d)
                b['film']=c
                tongji_film.append(b)
            else:
                for index, a1 in enumerate(tongji_film):
                    if row[0] == a1['name']:
                        mark = 0
                        for index2, a2 in enumerate(a1['film']):
                            if row[2]== a2['size']:
                                tongji_film[index]['film'][index2]['count'] = tongji_film[index]['film'][index2]['count'] + row[3]
                                mark =1
                        if mark == 0:
                            tongji_film[index]['film'].append({'size':row[2],'count':row[3]})


        tongji_film_count_list = [] #[{size:,count:},{size:,count:}]
        for row in tongji_films:
            #print(row)
            #row:['俞雪华', 'CT', '14INX17IN', 2]
            d={}
            if len(tongji_film_count_list)==0:
                d['size']=row[2]
                d['count']=row[3]
                tongji_film_count_list.append(d)
            else:
                mark = 0
                for index,a in enumerate(tongji_film_count_list):
                    if a['size']==row[2]:
                        tongji_film_count_list[index]['count']=tongji_film_count_list[index]['count']+row[3]
                        mark = 1
                if mark == 0:
                    tongji_film_count_list.append({'size':row[2],'count':row[3]})
        for a in tongji_film_count_list:
            tongji_film_count = tongji_film_count+a['size']+'('+str(a['count'])+')'
        print(tongji_film_count)

        tongji_film_total = [] #[{'name':,'film';'14INX17IN(4),8INX10IN'(5)}] 合并胶片统计成str
        for a in tongji_film:
            #print(a)
            c ={}
            c['name']=a['name']
            s=''
            for b in a['film']:
                s = s +b['size']+'('+str(b['count'])+')'
            c['film']=s
            tongji_film_total.append(c)

        #查询含modality的子项表
        selstr_tongji_detail = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'tj_getClinicalDoctor_bodypart_fee\',\'@sModality=1,@odtRegisterBegin=\'\'%s\'\',@odtRegisterEnd=\'\'%s\'\'\'' %(startDate,endDate)
        tongjiDetail=selSql(selstr_tongji_detail)

        #把胶片统计加到统计中去
        for index,tj in enumerate(tongji):
            mark = 0
            for tjfilm in tongji_film_total:
                if tj[0]==tjfilm['name']:
                    tongji[index].append(tjfilm['film'])
                    mark = 1
            if mark == 0:
                 tongji[index].append(' ')

        #合并总表和子项表
        for tj in tongji:
            temp = {}
            temp['tongji'] = tj
            t = []
            for tjDetail in tongjiDetail:
                if tjDetail[0] == tj[0]:
                    tjDetailtemp = tjDetail[1:6]
                    t.append(tjDetailtemp)
            temp['tongjiDetail'] = t
            tongjiall.append(temp)
            tongjicount[0] = tongjicount[0] + tj[1]
            tongjicount[1] = tongjicount[1] + tj[2]
            tongjicount[2] = tongjicount[2] + tj[3]
    context = {
        'table_tongjiall':tongjiall,
        'table_tongjicount':tongjicount,
        'table_startDate':startDate,
        'table_endDate':endDate,
        'table_tongji_film_count':tongji_film_count
    }
    return  render(request,'tablespacs/index.html',context)

def testjQuery(request):
    context = {
    }
    return  render(request,'tablespacs/testjQuery.html',context)

def ajax(request):
    if request.method == "POST":
        name_dict = [{'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}]
        return JsonResponse(name_dict,safe=False)
    else:
        context = { }
        return  render(request,'tablespacs/testAjax.html',context)

def grid(request):
    context = { }
    return  render(request,'tablespacs/testJQGrid.html',context)

def grid_data(request):
    #print(request.method())
    name_dict={"total": "2","page": "1","records": "30",  "rows" : [{"id":1, "cell":["1", "2016-10-16", "cell13","1000.0","0","1000.0",]}, {"id":2, "cell":["13", "2016-10-16", "cell13","1000.0","0","1000.0",]},{"id":3, "cell":["10", "2016-10-16", "cell13","1000.0","0","1000.0",]}, {"id":4, "cell":["15", "2016-10-16", "cell13","1000.0","0","1000.0",]},],"userdata":{"amount":3220,"tax":342,"total":3564,"name":"Totals:"}, }
    return JsonResponse(name_dict,safe=False)
#维护检查部位
def bodypartDic(request):
    #检查方式
    selmdlstr = 'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'dic_get_Modality\',\'\' '
    mdlstable = selSql(selmdlstr)
    mdls = []
    for a in mdlstable:
        mdls.append(a[2])

    # ajax 请求
    if request.method == "POST" and request.is_ajax():
        #检查部位
        if request.POST["posttype"] =="mdl":
            mdl = request.POST["mdl"]
            #费用
            selstr =  'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'dic_getbodypart_fee\',\'@sModality=\'\'%s\'\' \' '%mdl
            bodyparts = selSql(selstr)
            #胶片
            selstrfilm =  'SET NOCOUNT ON; EXEC  tj_P_RUN_PROCDURE_WITH_SELECTRETURN  \'dic_getbodypart_film\',\'@sModality=\'\'%s\'\' \' '%mdl
            bodypartsfilm = selSql(selstrfilm)

            bodyparts_list=[]  #[{bodypart_name:,film;},]
            bdt=[]
            for row in bodypartsfilm:
                if row[3]:
                    if row[1] not in bdt:
                        d={}
                        bdt.append(row[1])
                        d['bodypart_name']=row[1]
                        d['film']=row[2]+'('+str(row[3])+')'
                        bodyparts_list.append(d)
                    else:
                        for index,t in enumerate(bodyparts_list):
                            if t['bodypart_name']==row[1]:
                                bodyparts_list[index]['film']= bodyparts_list[index]['film']+','+row[2]+'('+str(row[3])+')'

            #添加胶片统计到统计表
            tj_bodyparts=[]
            for index,t in enumerate(bodyparts):
                mark = 0
                for a in bodyparts_list:
                    if t[0] ==a['bodypart_name']:
                        bodyparts[index].append(a['film'])
                        mark =1
                if mark ==0:
                    bodyparts[index].append('')
            return JsonResponse(bodyparts,safe=False)

        #提交修改:"部位-费用-胶片"
        if request.POST["posttype"] =="modify":
            print(request.POST)
            bodyparts = []
            #修改费用
            #insertstr =   'reg_insert_dic_bodypart_register_z @sModality=\'%s\',@sbodypart=\'%s\',@sfee =\'%s\',@sfilm=\'%s\' '%(request.POST["mdl"],request.POST["bodypart"],request.POST["fee"],request.POST["film_text"])
            #insertSql(insertstr)
            #修改部位
            filmlist = request.POST["film_text"].split(',')
            #删除原来部位对应的胶片记录
            delstrfilm =   'dic_delbodypart_film @sModality=\'%s\',@sbodypart=\'%s\' ' %(request.POST["mdl"],request.POST["bodypart"])
            insertSql(delstrfilm)
            for f in filmlist:
                filmSize = f[0:-3]
                filmCount =f[-2:-1]
                insertstr =   'dic_insbodypart_fee_film @sModality=\'%s\',@sbodypart=\'%s\',@sfee =\'%s\',@sfilmsize=\'%s\',@sfilmcounts=\'%s\' '%(request.POST["mdl"],request.POST["bodypart"],request.POST["fee"],filmSize,filmCount)
                insertSql(insertstr)
            return  JsonResponse(bodyparts,safe=False)
    else:
        context = {
                   "mdls":mdls}
        return  render(request,'tablespacs/bodypartDic.html',context)
