#!/usr/bin/env python

# ** Author: Salman Rakin **

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import datetime

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

    print("Request:")
    print(json.dumps(req, indent=4))

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
        password= parameters.get("password").strip()

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

        baseurl = "http://202.40.190.114:8084/BotAPI/ApplicationStatus?"
        yql_query = "SELECT DISTINCT appl_status_desc FROM ocasmn.vw_appl_sts_info WHERE application_id = '"+id+"'"
        #yql_query=yql_query+id
        #yql_query=yql_query+"'AND application_type_code IN (+appl_type_code+)AND createby = DECODE ("+"corp_flag_code+,'N',+user_id+,createby)"
        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query="select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Dhaka')"

        action="ApplicationStatus"
        yql_url = baseurl + urlencode({'q': yql_query})+ "&"+urlencode({'act': action})+ "&"+urlencode({'usname': username})+ "&"+urlencode({'paswd': password}) + "&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

        if data=={}:
            speech="Sorry! You do not have the rights to get information of ID:- "+id+". Try with Your Application ID."
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }



        a = data.get('Status')
        b = str(a[0].get('result'))

        # speech = "Hello. You Application staus is: Submitted from ARO.  Thanks !"

        if  b=='None':
            speech="Sorry! Not a valid Application ID."
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
        password= parameters.get("password").strip()

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

        baseurl = "http://202.40.190.114:8084/BotAPI/ApplicationStatus?"

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
        flg=str(a[0].get('flag'))
        b = str(a[1].get('result'))

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
        password=parameters.get("password").strip()

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

        baseurl = "http://202.40.190.114:8084/BotAPI/ApplicationStatus?"

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
        flg = str(a[0].get('flag'))
        b = str(a[1].get('result'))

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
        password=parameters.get("password").strip()

        match = auth(username, password)

        if match == False:
            return {
                "speech": "Sorry! Username or/and password is wrong! Please Start over!",
                "displayText": "Sorry! Username or/and password is wrong! Please Start over",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }
        #top_factor=2

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


        baseurl = "http://202.40.190.114:8084/BotAPI/ApplicationStatus?"

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

        yql_url = baseurl + urlencode({'q': yql_query}) + "&" + urlencode({'act': action}) + "&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)
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


        baseurl = "http://202.40.190.114:8084/BotAPI/ApplicationStatus?"

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

        yql_url = baseurl + urlencode({'q': yql_query}) + "&" + urlencode({'act': action}) + "&format=json"

        test_res = urlopen(yql_url).read()
        data = json.loads(test_res)

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


    speech = " Hello Shaun!! Today the weather in " + location.get('city') + " is : " + condition.get('text') + \
             ", and the temperature is " + temp + " " + "C" + ".  Thanks!!"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
