from flask import Flask,render_template,request,jsonify
import os
import shutil
import requests
from bs4 import BeautifulSoup
from datetime import datetime
app = Flask(__name__)

def index():    
    return render_template('pages/index.html')

def whois_scan():
    
    # URL of the website you want to scrape
    # url = 'https://who.is/whois/jkt48.com'
    url = 'https://who.is/whois/'+request.form['target-host']

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print out the title of the page
    response_body = soup.find_all('div', class_='queryResponseBody')
    registar_info={}
    important_dates={}
    name_servers=[]
    similiar_domains=[]
    for RI in response_body[0].find_all('div',class_="queryResponseBodyRow"):
        registar_info[RI.find("div",class_="queryResponseBodyKey").text]=RI.find("div",class_="queryResponseBodyValue").text.strip()
        # print("{}:{}".format(RI.find("div",class_="queryResponseBodyKey").text,RI.find("div",class_="queryResponseBodyValue").text.strip()))
    for ID in response_body[1].find_all('div',class_="queryResponseBodyRow"):
        important_dates[ID.find("div",class_="queryResponseBodyKey").text]=ID.find("div",class_="queryResponseBodyValue").text.strip()
        # print("{}:{}".format(ID.find("div",class_="queryResponseBodyKey").text,ID.find("div",class_="queryResponseBodyValue").text))
    for NS in response_body[2].find_all('div',class_="queryResponseBodyValue"):
        name_servers.append(NS.text.strip())
        # print("{}".format(NS.text))
    for SD in response_body[3].find("div",class_="queryResponseBodyValue").find_all("a"):
        similiar_domains.append(SD.text.strip())
        # print("{}".format(SD.text))
    print(registar_info)
    print(important_dates)
    print(name_servers)
    print(similiar_domains)
    return jsonify(
        registar_info,important_dates,name_servers,similiar_domains
    )

def subdomain_scan():
    current_datetime = datetime.now()
    # URL of the website you want to scrape
    # url = 'https://who.is/whois/jkt48.com'
    url = 'https://subdomainfinder.c99.nl/scans/'+current_datetime.strftime('%Y-%m-%d')+'/jkt48.com'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print out the title of the page
    result = soup.find_all('div', class_='able-responsive')
    print(result)
    return "done"


app.add_url_rule("/",'index',index)
app.add_url_rule("/whois-scan",'whois_scan',whois_scan,methods=['POST'])
app.add_url_rule("/subdomain-scan",'subdomain_scan',subdomain_scan)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)