import os
import sqlite3
from bottle import *

def page_file(root, filename):
    return static_file(filename, root=root)

def html(filename):
	filename += ".html"
	return static_file(filename, root="./html/")    

@get("/")
def man():
    return html("index")

@get("/login")
def login():
	return html("login")

@get("/spasibi")
def faq():
    return html("spasibi")

@get("/check")
def chk():
    for i in ['X-AppEngine-Country', 'From', 'Accept', 'User-Agent', 'Accept-Language', 'Referer', 'Authorization', 'Pragma']:
    	print("Auth HEADER!:", request.get_header(i, default='no_header'))
    return "OK"

@get("/link/<whereto>")
def redir(whereto):
    print(whereto)
    whereto = "https://"+whereto
    redirect(whereto)
    for i in range(100000):
        print("redirok")

#@get("/tryshortlink/<whereto>")


@get("/redir302")
def r():
    redirect("http://yandex.ru", code=302)

@get("/redir301")
def r():
    redirect("http://yandex.ru", code=301)

        
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
