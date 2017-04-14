from bottle import *
import os

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

@get("/faq")
def faq():
    return html("faq")

@get("/check")
def chk():
    for i in ['X-AppEngine-Country', 'From', 'Accept', 'User-Agent', 'Accept-Language', 'Referer', 'Authorization', 'Pragma']:
    	print("Auth HEADER!:", request.get_header(i, default='no_header'))
    return "OK"

@get("/redirtry/<whereto>")
def redir(whereto):
    print(whereto)
    whereto = "https://"+whereto
    redirect(whereto)
    for i in range(100000):
        print("redirok")

#@get("/tryshortlink/<whereto>")

        

@route("/<root>/<filename>")
def f(root, filename):
    return page_file(root, filename)

@route("/css/font-awesome/css/font-awesome.min.css")
def font():
    return static_file("font-awesome.min.css", root="./css/font-awesome/css/")

@route("/images/logo.png")
def logo():
    return static_file("logo.png", root='./images/')

    
run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=True)
