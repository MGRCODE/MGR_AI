import requests
import json
import streamlit as st
import pandas as pd

def abuseipddb_ioc_checker(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': f'{ip}',
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': 'c846e23da91e5b69573eeee2c651ced35bc58f609270f9509d13a2cd0d3a17df992537068b7ee425'
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    return response.json()

def bulk_abuseipddb_ioc_checker(iplist):
    url = 'https://api.abuseipdb.com/api/v2/check'

    

    headers = {
        'Accept': 'application/json',
        'Key': 'c846e23da91e5b69573eeee2c651ced35bc58f609270f9509d13a2cd0d3a17df992537068b7ee425'
    }
    iplist=iplist.split('\n')
    iplistresult=[]
    for ip in iplist[:1000]:
        querystring = {
        'ipAddress': f'{ip}',
        'maxAgeInDays': '90'
            }
        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        iplistresult.append(response.json()['data'])
    #print(iplistresult)
    #df=pd.read_json(iplistresult)
    return iplistresult
dftemp=df = pd.DataFrame(
    [
       {"ioc": ""},
   ]
)
st.header("Welcome to GaneshRaja Threat Intel")
bulkdflist=st.data_editor(dftemp)
bulkiocvalues=st.text_area("Enter Bulk IPs")
#iocvalue=st.text_input("Enter IOC")
iocvaluesubmit=st.button("submit")
if iocvaluesubmit or bulkiocvalues :
    #abuseipdbiocdetails=abuseipddb_ioc_checker(iocvalue)
    #st.json(abuseipdbiocdetails)
    bulkresult=bulk_abuseipddb_ioc_checker(bulkiocvalues)
    df=pd.DataFrame.from_dict(bulkresult)
    st.dataframe(df)


