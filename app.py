#!/usr/bin/env python

# ** Author: Salman Rakin **

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import datetime, timedelta

import json
import os
#import datetime
import re

from flask import Flask
from flask import request
from flask import make_response

status_code="01"
flag=1
flag1 =0
date1="01/01/2017"
date2="07/20/2017"

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "yahooWeatherForecast":

        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = makeYqlQuery(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        result = urlopen(yql_url).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res

    elif req.get("result").get("action")=="employee.info":
        result = req.get("result")
        cont = result.get("contexts")
        item_count = len(cont)
        index = -1

        for i in range(item_count):
            if cont[i]['name'] == 'emp_id':
                index = i

        if (index == -1):
            return {
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id = cont[0]['parameters']['emp_id.original']

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        # yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "employee.info"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode({'act': action}) + "&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data == {}:
            return {
                "speech": "Sorry!! No records found for the employee ID:- " + emp_id
            }
        else:
            return {
                "speech": "Welcome !!  "+data['Employee_name']+". How can I help you !!",
                "contextOut": [

                               {"name": "emp_id", "lifespan": 249, "parameters": {"emp_id.name": data['Employee_name']}}

                               ]
            }


    elif req.get("result").get("action")=="Leave.02":
        result=req.get("result")
        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index == -1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[0]['parameters']['emp_id.original']

        #print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        #yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.02"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode({'act': action}) +"&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data=={}:
            return{
                "speech": "Sorry!! No records found for the employee ID:- "+emp_id
            }

        leaves=""

        for i in range(1, len(data)):
            leaves += data['Leave' + str(i)] + " , "


        return {

            "speech": "Your available leaves are :-  "+leaves + " Thanks!"
        }


    elif req.get("result").get("action")=="Leave.03":
        result=req.get("result")
        parameters = result.get("parameters")
        leave_type=parameters.get("leave_type")

        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index==-1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[0]['parameters']['emp_id.original']

        print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        #yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.03"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" +urlencode({'leave_type':leave_type})+"&" +urlencode({'act': action}) +"&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data['Number of Rows']==0:
            return{
                "speech": "Sorry!! You're not eligible for "+leave_type+" ."
            }


        query_dict = data['Query']

        speech=""

        if data['Number of Rows']> 1:
            speech=" Here's your leave balance for all kind of leaves:-  "

            for key, value in query_dict.items():
                speech = speech+" .. " + key + " : " + value + " ;  "

            speech=speech+" Thanks!!"

            return {

                "speech": speech
            }
        else:

            for key,value in query_dict.items():
                leave_count=value;
            speech=" Your leave balance for "+leave_type+" is :- "+leave_count+". Thanks!!"

            return{

                "speech": speech
            }




    elif req.get("result").get("action")=="Leave.04":
        result=req.get("result")
        parameters = result.get("parameters")
        leave_type=parameters.get("leave_type")

        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index==-1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[0]['parameters']['emp_id.original']

        #print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        #yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.03"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" +urlencode({'leave_type':leave_type})+"&" +urlencode({'act': action}) +"&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data['Number of Rows']==0:
            return{
                "speech": "Sorry!! You're not eligible for "+leave_type+" ."
            }


        query_dict = data['Query']

        speech=""

        if data['Number of Rows']> 1:
            speech=" Here's your leave balance for all kind of leaves:-  "

            elig_lv=[]

            for key, value in query_dict.items():
                speech = speech+" .. " + key + " : " + value + " ;  "
                if int(value)>0:
                    elig_lv.append(key)


            if len(elig_lv)==0:
                speech=speech+" You're not eligible for any kind of Leave!!"
            else:
                speech = speech + " So, You can take "
                for i in range(len(elig_lv)):
                    speech=speech+ elig_lv[i]+" , "

            speech=speech+" Thanks!!"

            return {

                "speech": speech
            }
        else:

            for key,value in query_dict.items():
                leave_count=value;
            speech=" Your leave balance for "+leave_type+" is :- "+leave_count


            if int(leave_count)>0:
                speech=speech+". You're eligible for taking leave !!"
            else:
                speech=speech+". You can't take leave right now."

            return{

                "speech": speech
            }


    elif req.get("result").get("action")=="Leave.08":
        result=req.get("result")
        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index == -1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[0]['parameters']['emp_id.original']

        #print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        #yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.08"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode({'act': action}) +"&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data=={}:
            return{
                "speech": "Sorry!! No records found for the employee ID:- "+emp_id
            }

        if data['LFA_DATE']==None:
            speech="Sorry!! No records found for the employee ID:- "+emp_id
        else:
            speech="You will be eligible for LFA on:-  "+ data['LFA_DATE']


        return {

            "speech": speech
        }



    elif req.get("result").get("action")=="Leave.14":
        result=req.get("result")
        parameters = result.get("parameters")
        leave_type= parameters.get("leave_type")
        start_date = parameters.get("start_date")
        end_date = parameters.get("end_date")

        #print(start_date)
        #print(end_date)

        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index==-1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[i]['parameters']['emp_id.original']


        #print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        #yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.14"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" +urlencode({'leave_type':leave_type})+"&"+urlencode({'start_date':start_date})+"&"+urlencode({'end_date':end_date})+"&" +urlencode({'act': action}) +"&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data['Total_Approved_Person']==0:
            return{
                "speech": "Sorry!! No record found for Employee ID:- "+ emp_id
            }

        num = data['Total_Approved_Person']

        speech=" Number of approval person for your "+leave_type+" leave  is:- "+str(num)

        query_dict = data['Description']

        speech=speech+". They are:-  "

        for key, value in query_dict.items():
            speech = speech + " " + str(key) + ") " + value + " .. "

        speech=speech+" Thanks!!"


        return{

            "speech": speech
        }


    elif req.get("result").get("action")=="Leave.15":
        result=req.get("result")
        parameters = result.get("parameters")
        leave_type= parameters.get("leave_type")
        start_date = parameters.get("start_date")
        end_date = parameters.get("end_date")

        #print(start_date)
        #print(end_date)

        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index==-1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[i]['parameters']['emp_id.original']


        #print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        #yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.15"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" +urlencode({'leave_type':leave_type})+"&"+urlencode({'start_date':start_date})+"&"+urlencode({'end_date':end_date})+"&" +urlencode({'act': action}) +"&format=json"



        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)
        query_dict = data['Query']

        speech=""

        if data['Number of Leaves']==0:
            return{
                "speech": "Sorry!! No record found for Employee ID:- "+ emp_id
            }
        elif data['Number of Leaves']==1:

            speech="Your availed leave of "
            for key,value in query_dict.items():
                speech=speech+key+ " is:- "+ str(value)

            speech=speech+". Thanks!!"
            return{
                "speech": speech
            }
        else:
            speech=" Here's the details of your all kind of availed leaves:- "

            for key,value in query_dict.items():
                speech=speech + key+" : "+ value+"   ..   "

            speech = speech + "  Thanks!!"

            return {
                "speech": speech
            }


    elif req.get("result").get("action")=="Leave.16":

        result=req.get("result")
        parameters = result.get("parameters")
        time_frame=parameters.get("time_frame")


        #leave_type= parameters.get("leave_type")
        #start_date = parameters.get("start_date")
        #end_date = parameters.get("end_date")

        #print(start_date)
        #print(end_date)


        '''
        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index==-1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[i]['parameters']['emp_id.original']

        '''

        emp_id="000214"
        res=getDATE1(time_frame)




        #print(emp_id,time_frame,date1,date2)

        #print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"

        #yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.16"

        yql_url = baseurl + urlencode({'id': emp_id}) + "&" +urlencode({'time_frame':time_frame})+"&"+urlencode({'start_date':date1})+"&"+urlencode({'end_date':date2})+"&" +urlencode({'act': action}) +"&format=json"


        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)


        rec=[]

        #print(query_dict)

        #speech=""



        if data['Number of Records']==0:

            return{
                "speech": "No employees are in leave in "+time_frame+ ". Thanks!!"
            }

        else:

            speech = "Yes, Total " + str(data['Number of Records']) + " employees are on leave " + time_frame + "."

            print(speech)
            query_dict = data['Query']

            for i in range(data['Number of Records']):
                rec.append(query_dict['Record' + str(i + 1)])
                for key, value in rec[i].items():
                    speech = speech+" "+ value+ " "


            speech = speech + " Thanks!!"

            #print(speech)

            return {
                "speech": speech
            }



    elif req.get("result").get("action")=="Leave.17":

        result=req.get("result")
        parameters = result.get("parameters")
        time_frame=parameters.get("time_frame")
        #leave_type= parameters.get("leave_type")
        #start_date = parameters.get("start_date")
        #end_date = parameters.get("end_date")

        #print(start_date)
        #print(end_date)



        emp_id="000214"


        date_1= time_frame.split('/')[0]
        date_2 = time_frame.split('/')[1]




        #print(emp_id,time_frame,date1,date2)

        #print("Employee id:-",emp_id)

        #speech=

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"

        action = "Leave.17"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" +urlencode({'time_frame':time_frame})+"&"+urlencode({'start_date':date_1})+"&"+urlencode({'end_date':date_2})+"&" +urlencode({'act': action}) +"&format=json"



        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)


        rec=[]

        #print(query_dict)

        #speech=""



        if data['Number of Records']==0:

            return{
                "speech": "No employees are in leave in "+time_frame+ ". Thanks!!"
            }

        else:

            speech = "Yes, Total " + str(data['Number of Records']) + " employees are on leave. Here's the list:- "

            print(speech)
            query_dict = data['Query']

            for i in range(data['Number of Records']):
                rec.append(query_dict['Record' + str(i + 1)])
                for key, value in rec[i].items():
                    speech = speech+" "+ value+ " "


            speech = speech + " Thanks!!"

            #print(speech)

            return {
                "speech": speech
            }



    elif req.get("result").get("action")=="Lv.App.01":
        result=req.get("result")
        parameters = result.get("parameters")
        leave_type=parameters.get("Type_of_Leave")

        cont= result.get("contexts")
        item_count=len(cont)
        index=-1

        for i in range(item_count):
            if cont[i]['name']=='emp_id':
                index=i

        if(index==-1):
            return{
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id=cont[index]['parameters']['emp_id.original']

        print("Employee id:-",emp_id)

        # speech="Sure! Your Employee ID: "+emp_id+" is valid."
        #
        # return {
        #
        #     "speech": speech
        # }

        if leave_type=="":
            baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
            # yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
            # yql_query=yql_query+id
            # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
            # baseurl = "https://query.yahooapis.com/v1/public/yql?"
            # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

            action = "Leave.02"
            yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode({'act': action}) + "&format=json"

            test_res = urlopen(yql_url).read()
            data = json.loads(test_res)

            if data == {}:
                return {
                    "speech": "Sorry!! No records found for the employee ID:- " + emp_id + ". Probably "+ emp_id+" is not a valid ID."
                }

            leaves = ""

            for i in range(1, len(data)):
                leaves += data['Leave' + str(i)] + " , "

            return {

                "speech": "Sure. Your available leaves are :-  " + leaves + " Which leave you wanna take now ? "
            }

        else:

            if leave_type=='CL':
                leave_context='casuale_leave'
            elif leave_type=='EL' or leave_type=='LFA':
                leave_context='earn_leave'


            baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
            # yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
            # yql_query=yql_query+id
            # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
            # baseurl = "https://query.yahooapis.com/v1/public/yql?"
            # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

            action = "Leave.03"
            yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode(
                {'leave_type': leave_type}) + "&" + urlencode(
                {'act': action}) + "&format=json"

            test_res = urlopen(yql_url).read()
            data = json.loads(test_res)

            if data['Number of Rows'] == 0:
                return {
                    "speech": "Sorry!! You're not eligible for " + leave_type + " . Your leave blance of "+leave_type+" is: "+data['Number of Rows'],

                }

            query_dict = data['Query']

            speech = ""

            if data['Number of Rows'] > 1:
                speech = " Here's your leave balance for all kind of leaves:-  "

                for key, value in query_dict.items():
                    speech = speech + " .. " + key + " : " + value + " ;  "

                speech = speech + " Thanks!!"

                return {

                    "speech": speech
                }
            else:

                for key, value in query_dict.items():
                    leave_count = value;

                if leave_count == '0':
                    speech = "Sorry!! Your leave balance for " + leave_type + " is :- " + leave_count + " You can't take this leave right now!"
                    return {
                        "speech": speech,
                        "contextOut": [{"name": "date_param", "lifespan": 0, "parameters": {}},
                                   {"name": "leave_type", "lifespan": 0, "parameters": {}},
                                   {"name": "emp_id", "lifespan": 149, "parameters": {"emp_id.original":emp_id,"leave_balance":leave_count}},
                                   ]
                    }

                else:
                    speech = " Great!! Your leave balance for " + leave_type + " is :- " + leave_count + ". Now enter the FROM DATE of your leave "

                return {

                    "speech": speech,
                    "contextOut": [{"name": "date_param", "lifespan": 19, "parameters": {}},
                                   {"name": "leave_type", "lifespan": 14, "parameters": {"Type_of_Leave":leave_type}},
                                   {"name": "emp_id", "lifespan": 149, "parameters": {"emp_id.original":emp_id,"leave_balance":leave_count}},
                                   ]
                }



    if req.get("result").get("action") == "Lv.App.02":
        result = req.get("result")
        parameters = result.get("parameters")
        leave_type=parameters.get("Type_of_Leave")

        cont = result.get("contexts")
        item_count = len(cont)
        index = -1

        for i in range(item_count):
            if cont[i]['name'] == 'emp_id':
                index = i

        if (index == -1):
            return {
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id = cont[index]['parameters']['emp_id.original']

        print("Employee id:-", emp_id)

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        # yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Leave.03"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode({'leave_type': leave_type}) + "&" + urlencode(
            {'act': action}) + "&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data['Number of Rows'] == 0:
            return {
                "speech": "Sorry!! You're not eligible for " + leave_type + " ."
            }

        query_dict = data['Query']

        speech = ""

        if data['Number of Rows'] > 1:
            speech = " Here's your leave balance for all kind of leaves:-  "

            for key, value in query_dict.items():
                speech = speech + " .. " + key + " : " + value + " ;  "

            speech = speech + " Thanks!!"

            return {

                "speech": speech
            }
        else:

            if leave_type=='CL':
                leave_context='casuale_leave'
            elif leave_type=='EL' or leave_type=='LFA':
                leave_context='earn_leave'

            for key, value in query_dict.items():
                leave_count = value;

            if leave_count=='0':
                speech="Sorry!! Your leave balance for " + leave_type + " is :- " + leave_count + " You can't take this leave right now!!"

                return {

                    "speech":speech,
                    "contextOut": [{"name": "date_param", "lifespan": 0, "parameters": {}},
                                   {"name": "leave_type", "lifespan": 0, "parameters": {}},
                                   {"name": "emp_id", "lifespan": 149, "parameters": {"emp_id.original":emp_id}},
                                   ]
                }

            else:
                speech = " Great!! Your leave balance for " + leave_type + " is :- " + leave_count + ". Now enter the FROM DATE of your leave "

            return {

                "speech": speech,
                "contextOut": [
                               {"name": "emp_id", "lifespan": 149, "parameters": {"emp_id.original": emp_id,"leave_balance":leave_count}},
                               ]
            }

    if req.get("result").get("action") == "Lv.App.03":
        result = req.get("result")
        parameters = result.get("parameters")
        from_date=parameters.get("from_date")
        to_date=parameters.get("to_date")

        cont = result.get("contexts")
        item_count = len(cont)
        index = -1

        for i in range(item_count):
            if cont[i]['name'] == 'emp_id':
                index = i

        if (index == -1):
            return {
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id = cont[index]['parameters']['emp_id.original']
            leave_type=cont[index]['parameters']['Type_of_Leave']
            leave_balance=cont[index]['parameters']['leave_balance']
            leave_balance=int(leave_balance)

        # print("Employee id:-",emp_id)
        # print("Leave Type:-",leave_type)
        # print("from_date:-",from_date)
        # print("to_date:-",to_date)

        holiday= holiday_check(from_date,to_date)
        #speech=''


        if holiday['difference']>leave_balance:
            speech=" Oopss!! You have applied "+leave_type+" for "+ str(holiday['difference'])+" .But I have already showed your leave balance for "+leave_type+" is: "+str(leave_balance)+".So, Enter another FROM date to continue again!! "
            return {
                "speech": speech,
                "contextOut": [
                    {"name": 'replacement', "lifespan": 0, "parameters": {}}
                ]
            }

        if holiday['holiday_check']:

            if holiday['difference'] > 3:
                speech = "Sorry!! You should apply for a casual leave no longer than 3 days period. And Your specified date contains Holiday as well. So, Enter another FROM date to continue again!! "
                return {
                    "speech": speech,
                    "contextOut": [
                                   {"name": 'replacement', "lifespan": 0, "parameters": {}}
                                   ]
                }
            else:
                speech="Attention !! Your specified date contains Holiday. If you agree, Enter the employee ID of your replacement person. Or, Enter another FROM date to continue again!!  "
                return {
                    "speech":speech
                    # "contextOut": [
                    #                {"name": 'replacement', "lifespan": 0, "parameters": {}}
                    #                ]
                }
        else:
            if holiday['difference'] > 3:
                speech = "Sorry!! You should apply for a casual leave no longer than 3 days period. So, Enter another FROM date to continue again!! "
                return {
                    "speech": speech,
                    "contextOut": [
                                   {"name": 'replacement', "lifespan": 0, "parameters": {}}
                                   ]
                }

            else:
                baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
                # yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
                # yql_query=yql_query+id
                # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
                # baseurl = "https://query.yahooapis.com/v1/public/yql?"
                # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

                action = "Lv.App.03"
                yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode(
                    {'from_date': from_date}) + "&" + urlencode(
                    {'to_date': to_date}) + "&" + urlencode(
                    {'act': action}) + "&format=json"
                test_res = urlopen(yql_url).read()
                data = json.loads(test_res)

                if data['Result'] == '0':
                    return {
                        "speech": "Great! Now Enter the employee ID of your replacement person."
                    }
                else:
                    return {
                        "speech": "You already applied for a leave on the specified date you provided. Please Enter another FROM date to continue!",
                        "contextOut": [
                                        {"name": 'replacement', "lifespan": 0, "parameters": {}}
                                      ]
                    }


    if req.get("result").get("action") == "Lv.App.04":
        result = req.get("result")
        parameters = result.get("parameters")
        #from_date=parameters.get("from_date")
        #to_date=parameters.get("to_date")

        cont = result.get("contexts")
        item_count = len(cont)
        index = -1

        for i in range(item_count):
            if cont[i]['name'] == 'emp_id':
                index = i

        if (index == -1):
            return {
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id = cont[index]['parameters']['emp_id.original']
            leave_type=cont[index]['parameters']['Type_of_Leave']
            from_date= cont[index]['parameters']['from_date']
            to_date= cont[index]['parameters']['to_date']
            replacement_id= cont[index]['parameters']['replacement_id.original']

        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        # yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Lv.App.04"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&" + urlencode({'replacement_id': replacement_id}) + "&" + urlencode(
            {'from_date': from_date}) + "&" + urlencode(
            {'to_date': to_date}) + "&" + urlencode(
            {'act': action}) + "&format=json"
        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data['Result'] == '0':

            if data['Replacement_Status']=='Inactive':
                return {
                    "speech": "Oopss! I can't set" + data['Replacement_Name'] + " of ID: " + data['Replacement_ID'] + " as your replacement person. This employee might be inactive. You can Enter another replacment ID to continue ",
                    "contextOut": [
                        {"name": 'leave_info', "lifespan": 0, "parameters": {}}
                    ]
                }

            else:
                return {
                    "speech": "Awesome! This replacement person "+data['Replacement_Name']+" of ID: "+data['Replacement_ID']+ " is "+data['Replacement_Status']+". Enter 'Yes' to confirm this person as your replacement or Enter another ID to continue "
                }
        else:
            return {
                "speech": "Oh! Owe! Your replacement person " +data['Replacement_Name']+" of ID: "+data['Replacement_ID']+" is also in leave form "+from_date+" - "+to_date+". Please enter another replacement ID to continue!",
                "contextOut": [
                    {"name": 'leave_info', "lifespan": 0, "parameters": {}}
                ]
            }


    if req.get("result").get("action") == "Lv.App.05":
        result = req.get("result")
        parameters = result.get("parameters")
        #from_date=parameters.get("from_date")
        #to_date=parameters.get("to_date")

        cont = result.get("contexts")
        item_count = len(cont)
        index = -1

        for i in range(item_count):
            if cont[i]['name'] == 'emp_id':
                index = i

        if (index == -1):
            return {
                "speech": "No context named emp_id found. So, I can't proceed. Please contact developer."
            }
        else:
            emp_id = cont[index]['parameters']['emp_id.original']
            leave_type=cont[index]['parameters']['Type_of_Leave']
            from_date= cont[index]['parameters']['from_date']
            to_date= cont[index]['parameters']['to_date']
            replacement_id= cont[index]['parameters']['replacement_id.original']
            device_id= cont[index]['parameters']['device_id.original']
            session_id= cont[index]['parameters']['session_id.original']
            leave_purpose= cont[index]['parameters']['leave_purpose.original']
            contact_no= cont[index]['parameters']['contact_no.original']
            address= cont[index]['parameters']['address.original']
            emp_name= cont[index]['parameters']['emp_id.name']

        print(emp_id, leave_type,from_date,to_date,replacement_id,device_id,session_id,leave_purpose,contact_no,address)


        baseurl = "http://202.40.190.114:8084/BotAPI-HR/ApplicationStatus?"
        # yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '" + id + "'"
        # yql_query=yql_query+id
        # yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action = "Lv.App.05"
        yql_url = baseurl + urlencode({'id': emp_id}) + "&"+ urlencode({'leave_type': leave_type}) + "&"+ urlencode({'device_id': device_id}) + "&"+ urlencode({'session_id': session_id}) + "&" + urlencode({'leave_purpose': leave_purpose}) + "&"+ urlencode({'contact_no': contact_no}) + "&"+ urlencode({'address': address}) + "&" + urlencode({'replacement_id': replacement_id}) + "&" + urlencode(
            {'start_date': from_date}) + "&" + urlencode(
            {'end_date': to_date}) + "&" + urlencode(
            {'act': action}) + "&format=json"
        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data['Flag'] == 'N':
            return {
                "speech": "Sorry! Problem in Data Insertion. Reason: "+data['Message']+" Plese enter re-submit to try again!! "

            }
        elif data['Flag'] == 'Y':
            return {
                "speech": "Congratulations!!" + data['Message'] + " Enjoy your vacation, "+emp_name+" !!"
            }





    elif req.get("result").get("action") == "loan.eligibilty":

        result = req.get("result")
        parameters = result.get("parameters")
        zone = str(parameters.get("Numbers"))

        zone = zone.strip()
        # zone= int(zone)
        # val= int(zone)

        # condition['zone'] = int(zone)

        # cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
        # if zone is not None and zone.isnumeric():
        if int(zone) > 25000:
            speech = "Congratulation, Sir. You are eligible for loan"
        else:
            speech = "We're Sorry, Sir. You are not eligible for loan"

        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            # "data": {},
            # "contextOut": [],
            #"source": "apiai-onlinestore-shipping"
        }

    elif req.get("result").get("action") == "ApplicationStatus":


        result = req.get("result")
        parameters = result.get("parameters")
        id = parameters.get("ID")
        username=parameters.get("username").strip()
        username=username.replace(' ','.')

        if "href" in username:
            username = skype_auth(username)

        password = parameters.get("password").strip()

        if "herf" in password:
            password = skype_auth(password)

        match=False

        #match=auth(username,password)

        """
        if match==False:
            return {
                "speech": "Sorry! Username or/and password is wrong! Please Start Over!",
                "displayText": "Sorry! Username or/and password is wrong! Please Start Over!",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }

        """
        # id=id.strip()

        baseurl = "http://103.17.69.35:81/BotAPI/ApplicationStatus?"
        yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '"+id+"'"
        #yql_query=yql_query+id
        #yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action="ApplicationStatus"
        yql_url = baseurl + urlencode({'q': yql_query})+ "&"+urlencode({'act': action})+ "&"+urlencode({'usname': username})+ "&"+urlencode({'paswd': password}) + "&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)
        flg=str(data['Status']['flag']);
        b=str(data['Status']['result'])

        if data=={} and flg=="N":
            speech="Sorry! You do not have the rights to get information of ID:- "+id+". Try with Your Own Application ID."
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }
        elif data=={} and flg=="Y":
            speech="Sorry! "+id+" is not a valid application id."
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }



        #a = data.get('Status')
        #b = str(a[0].get('result'))

        # speech = "Hello. You Application staus is: Submitted from ARO.  Thanks !"

        if  b=='None' and flg=="N":
            speech="Sorry! You do not have the rights to get information of ID:- "+id+". Try with Your Own Application ID."
        elif b=='None' and flg=="Y":
            speech = "Sorry! " + id + " is not a valid application id."
        else:
            speech = b

        return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }


    elif req.get("result").get("action") == "Proposal.Count_AR":
        error_code = 0
        result = req.get("result")
        parameters = result.get("parameters")
        str1 = parameters.get("time")
        role = parameters.get("role")
        prop_action = parameters.get("proposal_action")
        branch_name = parameters.get("Branch_Name").strip()
        b_type = parameters.get("b_type").strip()
        username= parameters.get("username").strip()
        username = username.replace(' ', '.')

        if "href" in username:
            username = skype_auth(username)

        password = parameters.get("password").strip()

        if "herf" in password:
            password = skype_auth(password)

        '''
        match = auth(username, password)

        if match == False:
            return {
                "speech": "Sorry! Username or/and password is wrong! Please Start Over!",
                "displayText": "Sorry! Username or/and password is wrong! Please Start Over!",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }
        '''

        # str1=str1.strip()

        # global date1,date2
        # date1="01/01/2017"
        # date2="07/20/2017"

        # str1 = input("Enter the time frame\n")


        branch_factor = " "

        if "ALL" in branch_name.upper() or "EVERY" in branch_name.upper() or "ANY" in branch_name.upper():
            branch_factor = " "
        else:
            branch_factor = "AND (branch_code ='" + branch_name + "' OR UPPER(BRANCH_NAME) LIKE '%" + branch_name.upper() + "%')"

        if "BR" in b_type.upper():
            branch_factor = branch_factor + " AND NVL (agent_flg, 'Z') = 'N'"
        elif "AG" in b_type.upper():
            branch_factor = branch_factor + " AND NVL (agent_flg, 'Z') = 'Y'"
        elif "BOTH" in b_type.upper():
            branch_factor = branch_factor+" "
        elif "ALL" in b_type.upper():
            branch_factor = branch_factor+" "
        else:
            error_code = 1

        global status_code
        global flag1

        if (prop_action == "Submitted"):
            if (role.upper() == "ARO"):
                # global flag1,status_code
                status_code = "01"
                flag1 = 0
            elif (role.upper() == "RO" or role.upper() == "RM"):
                # global flag1, status_code
                status_code = "02"
                flag1 = 0
            elif (role.upper() == "BDM"):
                # global flag1, status_code
                status_code = "03"
                flag1 = 0
            elif (role.upper() == "CRM"):
                # global flag1, status_code
                status_code = "05"
                flag1 = 0
            elif (role.upper() == "CRM MANAGER"):
                # global flag1, status_code
                status_code = "08"
                flag1 = 0
            elif (role.upper() == "CRM HEAD"):
                # global flag1, status_code
                status_code = "11"
                flag1 = 0
            elif (role.upper() == "ALL" or role.upper() == "GENERAL" or role.upper() == "ANY"):
                # global flag1
                flag1 = 1
            else:
                error_code = 1
                flag1 = -1

        elif (prop_action == "Reviewed"):
            if (role.upper() == "CRM"):
                # global flag1, status_code
                status_code = "07"
                flag1 = 0
            elif (role.upper() == "BDM"):
                # global flag1, status_code
                status_code = "17"
                flag1 = 0
            elif (role.upper() == "CRM MANAGER"):
                # global flag1, status_code
                status_code = "10"
                flag1 = 0
            elif (role.upper() == "HEAD OF BUSINESS"):
                # global flag1, status_code
                status_code = "20"
                flag1 = 0
            elif (role.upper() == "ALL" or role.upper() == "GENERAL" or role.upper() == "ANY"):
                # global flag1
                flag1 = 2
            else:
                error_code = 1
                flag1 = -1

        elif (prop_action == "Rejected"):
            if (role.upper() == "CRM"):
                # global flag1, status_code
                status_code = "06"
                flag1 = 0
            elif (role.upper() == "BDM"):
                # global flag1, status_code
                status_code = "04"
                flag1 = 0
            elif (role.upper() == "CRM MANAGER"):
                # global flag1, status_code
                status_code = "09"
                flag1 = 0
            elif (role.upper() == "ALL" or role.upper() == "GENERAL" or role.upper() == "ANY"):
                # global flag1
                flag1 = 3
            else:
                error_code = 1
                flag1 = -1
        elif (prop_action == "Declined"):
            # global flag1, status_code
            status_code = "13"
            flag1 = 0
        elif (prop_action == "Approved"):
            # global flag1, status_code
            status_code = "12"
            flag1 = 0
        else:
            error_code = 1
            flag1 = -1

        def getDATE(str1):

            global date1, date2
            if (str1.upper() == "TODAY"):
                # global date1,date2
                date1 = datetime.datetime.now().strftime("%m/%d/%Y")
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")

            elif (str1.upper() == "THIS WEEK" or str1.upper() == "CURRENT WEEK"):
                # global date1,date2
                week = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().isoweekday() % 7)
                week = week.strftime("%m/%d/%Y")
                print(week)
                print(datetime.datetime.now().strftime("%m/%d/%Y"))
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
                date1 = week
            elif (str1.upper() == "THIS YEAR" or str1.upper() == "CURRENT YEAR"):
                # global date1,date2
                year = datetime.datetime.now()
                year = year.replace(day=1, month=1)
                year = year.strftime("%m/%d/%Y")
                print(year)
                print(datetime.datetime.now().strftime("%m/%d/%Y"))
                date1 = year
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
            elif (str1.upper() == "LAST YEAR" or str1.upper() == "PREVIOUS YEAR"):

                # global date1,date2
                flag = 1
                num = datetime.datetime.now().strftime("%Y")
                num_int = int(num) - 1
                year = datetime.datetime.now()
                year = year.replace(day=1, month=1, year=num_int)
                year = year.strftime("%m/%d/%Y")
                y_num = datetime.datetime.now()
                y_num = y_num.replace(day=1, month=1)
                y_num = y_num - datetime.timedelta(days=1)
                y_num = y_num.strftime("%m/%d/%Y")
                print(year)
                print(y_num)
                date1 = year
                date2 = y_num
            else:
                print("Not a known time frame...")

        res = getDATE1(str1)

        # id=id.strip()

        # date1="01/01/2017"
        # date2="07/20/2017"


        # USING STRING CONCATANATION METHOD ... Handled Branch Factors

        baseurl = "http://103.17.69.35:81/BotAPI/ApplicationStatus?"

        if flag1 == 1:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') " + branch_factor + " AND APPL_STATUS_CODE IN ('01','02','03','05','08','11')"
        elif flag1 == 2:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') " + branch_factor + " AND APPL_STATUS_CODE IN ('07','10','17','20')"
        elif flag1 == 3:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') " + branch_factor + " AND APPL_STATUS_CODE IN ('04','06','09')"
        elif flag1 == 0:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') " + branch_factor + " AND APPL_STATUS_CODE='" + status_code + "'"
        else:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') " + branch_factor

        action = "Proposal.Count"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        yql_url = baseurl + urlencode({'q': yql_query}) + "&" + urlencode({'act': action}) + "&" + urlencode({'usname': username}) + "&" + urlencode({'paswd': password}) + "&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        a = data.get('Status')
        flg = str(data['Status']['flag'])
        b = str(data['Status']['result'])

        # speech = "Hello. You Application staus is: Submitted from ARO.  Thanks !"

        if flg=="0":
            if (flag == 0):
                speech = " Sorry! Not a valid time frame"
            elif (error_code == 1):
                speech = "Sorry! Response unavailable due to some data mismatch."
            else:
                speech = "Number of proposals that have been " + prop_action + " by " + role + " during " + str1 +" in "+branch_name+ " is: " + b
        else:
            speech=b
        return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }


    elif req.get("result").get("action") == "Proposal.Count":



        error_code = 0
        result = req.get("result")
        parameters = result.get("parameters")
        str1= parameters.get("time")
        role = parameters.get("role")
        prop_action=parameters.get("proposal_action")
        branch_name=parameters.get("Branch_Name").strip()
        b_type=parameters.get("b_type").strip()
        username=parameters.get("username").strip()
        username = username.replace(' ', '.')

        if "href" in username:
            username = skype_auth(username)

        password = parameters.get("password").strip()

        if "herf" in password:
            password = skype_auth(password)

        #match = False

        #match=auth(username, password)

        '''
        if match == False:
            return {
                "speech": "Sorry! Username or/and password is wrong! Please Start Over!!",
                "displayText": "Sorry! Username or/and password is wrong! Please Start Over!",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }
        '''

        #str1=str1.strip()

        #global date1,date2
        #date1="01/01/2017"
        #date2="07/20/2017"

        #str1 = input("Enter the time frame\n")


        branch_factor=" "

        if "ALL" in branch_name.upper()or "EVERY" in branch_name.upper() or"ANY" in branch_name.upper():
            branch_factor=" "
        else:
            branch_factor="AND (branch_code ='"+branch_name+"' OR UPPER(BRANCH_NAME) LIKE '%"+branch_name.upper()+"%')"

        if "BR" in b_type.upper():
            branch_factor=branch_factor+" AND NVL (agent_flg, 'Z') = 'N'"
        elif "AG" in b_type.upper():
            branch_factor = branch_factor + " AND NVL (agent_flg, 'Z') = 'Y'"
        elif "BOTH" in b_type.upper():
            branch_factor=branch_factor+" "
        elif "BOTH" in b_type.upper():
            branch_factor =branch_factor+ " "
        else:
            error_code=1


        #global status_code
        #global flag1

        if(prop_action=="Submitted"):
            if (role.upper() == "ARO"):
                #global flag1,status_code
                status_code="01"
                flag1=0
            elif (role.upper() == "RO" or role.upper() == "RM" ):
                #global flag1, status_code
                status_code = "02"
                flag1 = 0
            elif (role.upper() == "BDM"):
                #global flag1, status_code
                status_code = "03"
                flag1 = 0
            elif (role.upper() == "CRM"):
                #global flag1, status_code
                status_code = "05"
                flag1 = 0
            elif (role.upper() == "CRM MANAGER"):
                #global flag1, status_code
                status_code = "08"
                flag1 = 0
            elif (role.upper() == "CRM HEAD"):
                #global flag1, status_code
                status_code = "11"
                flag1 = 0
            elif (role.upper() == "ALL" or role.upper() == "GENERAL" or role.upper()=="ANY" ):
                #global flag1
                flag1=1
            else:
                error_code=1
                flag1 = -1

        elif (prop_action == "Reviewed"):
            if (role.upper() == "CRM"):
                #global flag1, status_code
                status_code = "07"
                flag1 = 0
            elif (role.upper() == "BDM"):
                #global flag1, status_code
                status_code = "17"
                flag1 = 0
            elif (role.upper() == "CRM MANAGER"):
                #global flag1, status_code
                status_code = "10"
                flag1 = 0
            elif (role.upper() == "HEAD OF BUSINESS"):
                #global flag1, status_code
                status_code = "20"
                flag1 = 0
            elif (role.upper() == "ALL" or role.upper() == "GENERAL" or role.upper()=="ANY" ):
                #global flag1
                flag1=2
            else:
                error_code = 1
                flag1 = -1

        elif (prop_action == "Rejected"):
            if (role.upper() == "CRM"):
                #global flag1, status_code
                status_code = "06"
                flag1 = 0
            elif (role.upper() == "BDM"):
                #global flag1, status_code
                status_code = "04"
                flag1 = 0
            elif (role.upper() == "CRM MANAGER"):
                #global flag1, status_code
                status_code = "09"
                flag1 = 0
            elif (role.upper() == "ALL" or role.upper() == "GENERAL" or role.upper()=="ANY" ):
                #global flag1
                flag1=3
            else:
                error_code = 1
                flag1 = -1
        elif (prop_action == "Declined"):
            #global flag1, status_code
            status_code = "13"
            flag1 = 0
        elif (prop_action == "Approved"):
            #global flag1, status_code
            status_code = "12"
            flag1 = 0
        else:
            error_code=1
            flag1=-1



        def getDATE(str1):

            global date1, date2
            if (str1.upper() == "TODAY"):
                #global date1,date2
                date1 = datetime.datetime.now().strftime("%m/%d/%Y")
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")

            elif (str1.upper() == "THIS WEEK" or str1.upper() == "CURRENT WEEK"):
                #global date1,date2
                week = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().isoweekday() % 7)
                week = week.strftime("%m/%d/%Y")
                print(week)
                print(datetime.datetime.now().strftime("%m/%d/%Y"))
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
                date1 = week
            elif (str1.upper() == "THIS YEAR" or str1.upper() == "CURRENT YEAR"):
                #global date1,date2
                year = datetime.datetime.now()
                year = year.replace(day=1, month=1)
                year = year.strftime("%m/%d/%Y")
                print(year)
                print(datetime.datetime.now().strftime("%m/%d/%Y"))
                date1 = year
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
            elif (str1.upper() == "LAST YEAR" or str1.upper() == "PREVIOUS YEAR"):

                #global date1,date2
                flag = 1
                num = datetime.datetime.now().strftime("%Y")
                num_int = int(num) - 1
                year = datetime.datetime.now()
                year = year.replace(day=1, month=1, year=num_int)
                year = year.strftime("%m/%d/%Y")
                y_num = datetime.datetime.now()
                y_num = y_num.replace(day=1, month=1)
                y_num = y_num - datetime.timedelta(days=1)
                y_num = y_num.strftime("%m/%d/%Y")
                print(year)
                print(y_num)
                date1 = year
                date2 = y_num
            else:
                print("Not a known time frame...")


        res=getDATE1(str1)


        # id=id.strip()

        #date1="01/01/2017"
        #date2="07/20/2017"


        # USING STRING CONCATANATION METHOD ... Handled Branch Factors

        baseurl = "http://103.17.69.35:81/BotAPI/ApplicationStatus?"

        if flag1==1:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') "+branch_factor+" AND APPL_STATUS_CODE IN ('01','02','03','05','08','11')"
        elif flag1==2:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') "+branch_factor+" AND APPL_STATUS_CODE IN ('07','10','17','20')"
        elif flag1==3:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') "+branch_factor+" AND APPL_STATUS_CODE IN ('04','06','09')"
        elif flag1==0:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('"+date1+"','MM-DD-YYYY') AND TO_DATE('"+date2+"','MM-DD-YYYY') "+branch_factor+" AND APPL_STATUS_CODE='"+status_code+"'"
        else:
            yql_query = "SELECT COUNT(DISTINCT APPLICATION_ID) AS N0_OF_PROPOSAL FROM OCASMN.VW_APPL_STS_INFO WHERE ARO_SUBMIT_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY') "+branch_factor

        action="Proposal.Count"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        yql_url = baseurl + urlencode({'q': yql_query}) + "&" + urlencode({'act': action}) + "&" + urlencode({'usname': username}) + "&" + urlencode({'paswd': password}) + "&format=json"
        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        a = data.get('Status')
        flg = str(data['Status']['flag'])
        b = str(data['Status']['result'])

        # speech = "Hello. You Application staus is: Submitted from ARO.  Thanks !"

        if flg == "0":
            if (flag == 0):
                speech = " Sorry! Not a valid time frame"
            elif (error_code == 1):
                speech = "Sorry! Response unavailable due to some data mismatch."
            else:
                speech = "Number of proposals that have been " + prop_action + " by " + role + " during " + str1 + " in " + branch_name + " is: " + b
        else:
            speech = b

        return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }


    elif req.get("result").get("action") == "Performance.top":

        error_code = 0
        result = req.get("result")
        parameters = result.get("parameters")
        str1 = parameters.get("time")
        role = parameters.get("role")
        branch_name = parameters.get("Branch_Name")
        type = parameters.get("type").strip()
        type_flag = ""
        top_factor= int(parameters.get("number"))

        username= parameters.get("username").strip()
        username = username.replace(' ', '.')


        if "href" in username:
           username=skype_auth(username)


        password = parameters.get("password").strip()

        if "herf" in password:
            password=skype_auth(password)

        #match = auth(username, password)

        """
        if match == False:
            return {
                "speech": "Sorry! Username or/and password is wrong! Please Start over!",
                "displayText": "Sorry! Username or/and password is wrong! Please Start over",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }
        #top_factor=2
        """
        branch_code = ""
        # str1=str1.strip()

        # global date1,date2
        # date1="01/01/2017"
        # date2="07/20/2017"

        # str1 = input("Enter the time frame\n")

        # global status_code
        # global flag1
        role_flag = 1
        error_code = 0

        if "BR" in type.upper():
            type_flag = 'N'
        elif "AG" in type.upper():
            type_flag = 'Y'
        elif "BOTH" in type.upper():
            branch_factor = " "
        elif "ALL" in type.upper():
            branch_factor = " "
        else:
            error_code = 1

        # type_flag='N'



        if (role.upper() == "CRM HEAD"):
            role = "CRMHED"
        elif (role.upper() == "HEAD OF BUSINESS"):
            role = "CMSEHOB"
        elif (role.upper() == "CRMS"):
            role = "CRMS"
        elif (role.upper() == "MD"):
            role = "MD"
        elif (role.upper() == "RM"):
            role = "RM"
        elif (role.upper() == "RO"):
            role = "RO"
        elif (role.upper() == "CRO"):
            role = "CRM"
        elif (role.upper() == "ARO"):
            role = "ARO"
        elif (role.upper() == "BDM"):
            role = "BDM"
        else:
            role_flag = 0

        res = getDATE1(str1)

        # date1 = "01/01/2016"
        # date2 = "12/31/2016"

        if error_code == 1:
            return {
                "speech": "Sorry! Response unavailable due to some data mismatch.",
                "displayText": "Sorry! Response unavailable due to some data mismatch.",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }

        # USING IF-ELSE CHAIN METHOD ... Handling Branch Factors


        baseurl = "http://103.17.69.35:81/BotAPI/ApplicationStatus?"

        if "ALL" in branch_name.upper() or "EVERY" in branch_name.upper() or "ANY" in branch_name.upper():

            if type.upper() == "BOTH" or  type.upper() == "ALL":
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role + "' AND appl_status_code = 12"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"

            else:
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role + "' AND appl_status_code = 12 AND NVL (agent_flg, 'Z') = '" + type_flag + "'"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"

        else:

            if type.upper() == "BOTH" or type.upper() == "ALL":
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role + "' AND appl_status_code = 12 AND (branch_code ='" + branch_name.strip() + "' OR UPPER(BRANCH_NAME) LIKE'%" + branch_name.strip().upper() + "%')"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"
            else:
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role + "' AND appl_status_code = 12 AND NVL (agent_flg, 'Z') = '" + type_flag + "' AND (branch_code ='" + branch_name.strip() + "' OR UPPER(BRANCH_NAME) LIKE'%" + branch_name.strip().upper() + "%')"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"

        action = "Performance.individual"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"


        yql_url = baseurl + urlencode({'q': yql_query}) + "&" + urlencode({'act': action}) + "&" + urlencode({'usname': username}) + "&" + urlencode({'paswd': password}) + "&format=json"


        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)
        result_top=str(data["Result"])

        if result_top!="OK":
            return {
                "speech": result_top,
                "displayText": result_top,
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }

        else:
            no_of_rows = data["Number of Rows"]

            if no_of_rows==0:
                final_speech="Sorry!! No records found for "+ role+ " in "+ branch_name+". Thanks!"
                return {
                    "speech": final_speech,
                    "displayText": final_speech,
                    # "data": data,
                    # "contextOut": [],
                    "source": "apiai-weather-webhook-sample"
                }


            if top_factor<= no_of_rows:
                no_of_rows = top_factor



            speech_counter = ""
            final_speech = ""

            for i in range(1, no_of_rows+ 1):
                final_speech = speech_counter +str(i)+". User ID: " + data['Query']['Row' + str(i)]['USER_ID']
                final_speech = final_speech + ",  Number of Approval: " + data['Query']['Row' + str(i)][
                    'PERFORMNC']
                final_speech = final_speech + ",  Branch Name " + data['Query']['Row' + str(i)]['BRANCH_NAME']
                final_speech = final_speech + ",  Requested_Amount: " + data['Query']['Row' + str(i)][
                    'REQUESTED_AMOUNT']
                final_speech = final_speech + ",  Approved_Amount: " + data['Query']['Row' + str(i)][
                    'APPROVE_AMOUNT'] + "     "
                speech_counter = final_speech

            return {
                "speech": final_speech,
                "displayText": final_speech,
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }

    elif req.get("result").get("action") == "Performance.individual":

        error_code = 0
        result = req.get("result")
        parameters = result.get("parameters")
        str1 = parameters.get("time")
        role = parameters.get("role")
        branch_name = parameters.get("Branch_Name")
        type=parameters.get("type").strip()
        username = parameters.get("username").strip()
        username = username.replace(' ', '.')

        if "href" in username:
            username = skype_auth(username)

        password = parameters.get("password").strip()

        if "herf" in password:
            password = skype_auth(password)


        type_flag=""
        branch_code=""
        # str1=str1.strip()

        # global date1,date2
        # date1="01/01/2017"
        # date2="07/20/2017"

        # str1 = input("Enter the time frame\n")

        #global status_code
        #global flag1
        role_flag = 1
        error_code=0

        if "BR" in type.upper():
            type_flag='N'
        elif "AG" in type.upper():
            type_flag='Y'
        elif "BOTH" in type.upper():
            branch_factor=" "
        elif "ALL" in type.upper():
            branch_factor = " "
        else:
            error_code=1

        #type_flag='N'



        if (role.upper() == "CRM HEAD"):
            role = "CRMHED"
        elif (role.upper() == "HEAD OF BUSINESS"):
            role = "CMSEHOB"
        elif (role.upper() == "CRMS"):
            role = "CRMS"
        elif (role.upper() == "MD"):
            role = "MD"
        elif (role.upper() == "RM"):
            role = "RM"
        elif (role.upper() == "RO"):
            role = "RO"
        elif (role.upper() == "CRO"):
            role = "CRM"
        elif (role.upper() == "ARO"):
            role = "ARO"
        elif (role.upper() == "BDM"):
            role = "BDM"
        else:
            role_flag = 0

        res = getDATE1(str1)

        #date1 = "01/01/2016"
        #date2 = "12/31/2016"

        if error_code==1:
            return {
                "speech": "Sorry! Response unavailable due to some data mismatch.",
                "displayText": "Sorry! Response unavailable due to some data mismatch.",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }


        # USING IF-ELSE CHAIN METHOD ... Handling Branch Factors


        baseurl = "http://103.17.69.35:81/BotAPI/ApplicationStatus?"

        if "ALL" in branch_name.upper() or "EVERY" in branch_name.upper() or "ANY" in branch_name.upper():

            if type.upper()=="BOTH" or type.upper()=="ALL":
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role +"' AND appl_status_code = 12"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"

            else:
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role + "' AND appl_status_code = 12 AND NVL (agent_flg, 'Z') = '" + type_flag + "'"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"

        else:

            if type.upper() == "BOTH" or type.upper() == "ALL":
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role + "' AND appl_status_code = 12 AND (branch_code ='" + branch_name.strip() + "' OR UPPER(BRANCH_NAME) LIKE'%" + branch_name.strip().upper() + "%')"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"
            else:
                yql_query = "SELECT   COUNT (application_id) AS performnc,TO_CHAR (NVL (SUM (req_limit), 0),'9999999999,990.99') || ' Milion' requested_amount,"
                yql_query = yql_query + "TO_CHAR (NVL (SUM (approve_limit), 0), '9999999999,990.99')|| ' Milion' approve_amount, createby user_id, branch_name"
                yql_query = yql_query + " FROM OCASMN.VW_APPL_STS_INFO"
                yql_query = yql_query + " WHERE user_group_code = '" + role + "' AND appl_status_code = 12 AND NVL (agent_flg, 'Z') = '" + type_flag + "' AND (branch_code ='" + branch_name.strip() + "' OR UPPER(BRANCH_NAME) LIKE'%" + branch_name.strip().upper() + "%')"
                yql_query = yql_query + " AND SUBMISSION_DT BETWEEN TO_DATE('" + date1 + "','MM-DD-YYYY') AND TO_DATE('" + date2 + "','MM-DD-YYYY')"
                yql_query = yql_query + "GROUP BY createby, branch_name ORDER BY performnc DESC"






        action = "Performance.individual"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"


        yql_url = baseurl + urlencode({'q': yql_query}) + "&" + urlencode({'act': action}) + "&" + urlencode({'usname': username}) + "&" + urlencode({'paswd': password}) + "&format=json"


        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)
        result_top = str(data["Result"])

        if result_top != "OK":
            return {
                "speech": result_top,
                "displayText": result_top,
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }

        else:


            no_of_rows = data["Number of Rows"]

            if no_of_rows==0:
                final_speech="Sorry!! No records found for "+ role+ " in "+ branch_name+". Thanks!"
                return {
                    "speech": final_speech,
                    "displayText": final_speech,
                    # "data": data,
                    # "contextOut": [],
                    "source": "apiai-weather-webhook-sample"
                }

            speech_counter = ""
            final_speech=""

            for i in range(1, no_of_rows + 1):
                final_speech = speech_counter +str(i)+". User ID: " + data['Query']['Row' + str(i)]['USER_ID']
                final_speech=final_speech+",  Number of Approval: " + data['Query']['Row' + str(i)]['PERFORMNC']
                final_speech=final_speech+",  Branch Name " + data['Query']['Row' + str(i)]['BRANCH_NAME']
                final_speech=final_speech+",  Requested_Amount: " + data['Query']['Row' + str(i)]['REQUESTED_AMOUNT']
                final_speech=final_speech+",  Approved_Amount: " + data['Query']['Row' + str(i)]['APPROVE_AMOUNT'] + "     "
                speech_counter=final_speech





            return {
                "speech": final_speech,
                "displayText": final_speech,
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }


    else:
        return {}



def skype_auth(username):
    start = username.find('"mailto:') + 8
    end = username.find('".title', start)
    uname=username[start:end]
    return uname

def auth(username,password):


    if(username=="rakin@bankasia net" or username=="rakin@bankasia.net" or username=="rakin" ):
        if(password=="123"):
                return True
        else:
            return False
    elif(username=="anwar@bankasia net" or username=="anwar@bankasia.net" or username=="anwar" ):
        if(password=="456"):
            return True
        else:
            return False

    else:
        return False

def getDATE1(str1):

            global date1, date2,flag
            if (str1.upper() == "TODAY"):

                flag=1
                date1 = datetime.datetime.now().strftime("%m/%d/%Y")
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
                # print(tod)
                return datetime.datetime.now().strftime("%m/%d/%Y")

            elif (str1.upper() == "YESTERDAY" or str1.upper() == "LAST DAY" or str1.upper() == "PREVIOUS DAY"):

                flag = 1
                yest = datetime.datetime.now() - datetime.timedelta(days=1)
                yest = yest.strftime("%m/%d/%Y")
                print(yest)
                date1 = yest
                date2 = yest
                return yest

            elif (str1.upper() == "DAY BEFORE YESTERDAY"):

                flag = 1
                yest = datetime.datetime.now() - datetime.timedelta(days=2)
                yest = yest.strftime("%m/%d/%Y")
                print(yest)
                date1 = yest
                date2 = yest
                return yest

            elif (str1.upper() == "THIS WEEK" or str1.upper() == "CURRENT WEEK"):

                flag = 1
                week = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().isoweekday() % 7)
                week = week.strftime("%m/%d/%Y")
                print(week)
                print(datetime.datetime.now().strftime("%m/%d/%Y"))
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
                date1 = week
                return week

            elif (str1.upper() == "LAST WEEK" or str1.upper() == "PREVIOUS WEEK"):

                flag = 1
                week = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().isoweekday() % 7)
                week_last = week - datetime.timedelta(days=7)
                week1 = week_last + datetime.timedelta(days=6)
                week_last = week_last.strftime("%m/%d/%Y")
                week1 = week1.strftime("%m/%d/%Y")
                print(week_last)
                print(week1)
                date1 = week_last
                date2 = week1
                return week_last

            elif (str1.upper() == "THIS MONTH" or str1.upper() == "CURRENT MONTH"):

                flag = 1
                month = datetime.datetime.now()
                month = month.replace(day=1)
                month = month.strftime("%m/%d/%Y")
                print(month)
                print(datetime.datetime.now().strftime("%m/%d/%Y"))
                date1 = month
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
                return month

            elif (str1.upper() == "LAST MONTH" or str1.upper() == "PREVIOUS MONTH"):

                flag = 1
                num = datetime.datetime.now().strftime("%m")
                num_int = int(num)
                num_int = num_int - 1
                # num = str(num_int - 1)
                month = datetime.datetime.now()
                month = month.replace(day=1, month=num_int)
                month = month.strftime("%m/%d/%Y")
                l_num = datetime.datetime.now()
                l_num = l_num.replace(day=1)
                l_num = l_num - datetime.timedelta(days=1)
                l_num = l_num.strftime("%m/%d/%Y")
                print(month)
                print(l_num)

                date1 = month
                date2 = l_num

                return month

            elif (str1.upper() == "THIS YEAR" or str1.upper() == "CURRENT YEAR"):

                flag = 1
                year = datetime.datetime.now()
                year = year.replace(day=1, month=1)
                year = year.strftime("%m/%d/%Y")
                print(year)
                print(datetime.datetime.now().strftime("%m/%d/%Y"))
                date1 = year
                date2 = datetime.datetime.now().strftime("%m/%d/%Y")
                return year

            elif (str1.upper() == "LAST YEAR" or str1.upper() == "PREVIOUS YEAR"):

                flag = 1
                num = datetime.datetime.now().strftime("%Y")
                num_int = int(num) - 1
                year = datetime.datetime.now()
                year = year.replace(day=1, month=1, year=num_int)
                year = year.strftime("%m/%d/%Y")
                y_num = datetime.datetime.now()
                y_num = y_num.replace(day=1, month=1)
                y_num = y_num - datetime.timedelta(days=1)
                y_num = y_num.strftime("%m/%d/%Y")
                print(year)
                print(y_num)
                date1 = year
                date2 = y_num

                return year

            elif (str1.upper() == "FIRST QUARTER" or str1.upper() == "1ST QUARTER"):

                flag = 1
                quat = datetime.datetime.now()
                quat = quat.replace(day=1, month=1)
                quat = quat.strftime("%m/%d/%Y")
                print(quat)
                date1 = quat

                quat1 = datetime.datetime.now()
                quat1 = quat1.replace(day=1, month=4)
                quat1 = quat1 - datetime.timedelta(days=1)
                quat1 = quat1.strftime("%m/%d/%Y")
                print(quat1)
                date2 = quat1

                return quat

            elif (str1.upper() == "SECOND QUARTER" or str1.upper() == "2ND QUARTER"):

                flag = 1
                quat1 = datetime.datetime.now()
                quat1 = quat1.replace(day=1, month=4)
                # quat1 = quat1 - datetime.timedelta(days=1)
                quat1 = quat1.strftime("%m/%d/%Y")
                print(quat1)

                date1 = quat1

                quat2 = datetime.datetime.now()
                quat2 = quat2.replace(day=1, month=7)
                quat2 = quat2 - datetime.timedelta(days=1)
                quat2 = quat2.strftime("%m/%d/%Y")
                print(quat2)

                date2 = quat2
                return quat2

            elif (str1.upper() == "THIRD QUARTER" or str1.upper() == "3RD QUARTER"):

                flag = 1
                quat1 = datetime.datetime.now()
                quat1 = quat1.replace(day=1, month=7)
                # quat1 = quat1 - datetime.timedelta(days=1)
                quat1 = quat1.strftime("%m/%d/%Y")
                print(quat1)

                date1 = quat1

                quat2 = datetime.datetime.now()
                quat2 = quat2.replace(day=1, month=10)
                quat2 = quat2 - datetime.timedelta(days=1)
                quat2 = quat2.strftime("%m/%d/%Y")
                print(quat2)

                date2 = quat2
                return quat2

            elif (str1.upper() == "FOURTH QUARTER" or str1.upper() == "4TH QUARTER"):

                flag = 1
                quat1 = datetime.datetime.now()
                quat1 = quat1.replace(day=1, month=10)
                # quat1 = quat1 - datetime.timedelta(days=1)
                quat1 = quat1.strftime("%m/%d/%Y")
                print(quat1)
                date1 = quat1
                year = datetime.datetime.now().strftime("%Y")
                year_int = int(year) + 1
                quat2 = datetime.datetime.now()
                quat2 = quat2.replace(day=1, month=1, year=year_int)
                quat2 = quat2 - datetime.timedelta(days=1)
                quat2 = quat2.strftime("%m/%d/%Y")
                print(quat2)
                date2 = quat2
                return quat2

            elif (str1.upper() == "HALF YEARLY"):

                flag = 1
                year = datetime.datetime.now().strftime("%m")
                count = int(year)

                if count > 6:
                    quat1 = datetime.datetime.now()
                    quat1 = quat1.replace(day=1, month=7)
                    # quat1 = quat1 - datetime.timedelta(days=1)
                    quat1 = quat1.strftime("%m/%d/%Y")
                    print(quat1)
                    date1 = quat1

                    year = datetime.datetime.now().strftime("%Y")
                    year_int = int(year) + 1
                    quat2 = datetime.datetime.now()
                    quat2 = quat2.replace(day=1, month=1, year=year_int)
                    quat2 = quat2 - datetime.timedelta(days=1)
                    quat2 = quat2.strftime("%m/%d/%Y")
                    print(quat2)
                    date2 = quat2
                else:
                    quat1 = datetime.datetime.now()
                    quat1 = quat1.replace(day=1, month=1)
                    # quat1 = quat1 - datetime.timedelta(days=1)
                    quat1 = quat1.strftime("%m/%d/%Y")
                    print(quat1)
                    date1 = quat1
                    quat2 = datetime.datetime.now()
                    quat2 = quat2.replace(day=1, month=7)
                    quat2 = quat2 - datetime.timedelta(days=1)
                    quat2 = quat2.strftime("%m/%d/%Y")
                    print(quat2)
                    date2 = quat2
                return quat2

            else:
                flag=0
                print("Not a known time frame...")

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    temp= condition.get('temp')
    temp=int(temp)
    temp = ((temp-32)*5)/9
    temp=str(temp)


    speech = " Hello !! Today the weather in " + location.get('city') + " is : " + condition.get('text') + \
             ", and the temperature is " + temp + " " + "C" + ".  Thanks!!"

    print("Final Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def holiday_check(from_date,to_date):

    date_format = "%Y-%m-%d"
    from_date = datetime.strptime(from_date, date_format)
    to_date = datetime.strptime(to_date, date_format)
    delta = to_date - from_date

    data = {}

    diff = delta.days + 1

    data['difference'] = diff

    #holiday_status=False

    #print (delta.days)

    day=0

    if delta.days == 0:
        day= from_date.weekday()

    #print('Day: ',day)

    if day==4 or day==5:
        holiday_status=True
        data['holiday_check'] = holiday_status
        return data
        #return holiday_status


    fromdate=from_date
    todate=to_date

    daygenerator = (fromdate + timedelta(x + 1) for x in range((todate - fromdate).days))

    hol_delta=sum(1 for day in daygenerator if day.weekday() < 5)

    if(delta.days>hol_delta):
        holiday_status=True
        #return holiday_status
    else:
        holiday_status=False
        #return holiday_status

    data['holiday_check'] = holiday_status
    return data

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
