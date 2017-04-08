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

@route("/<root>/<filename>")
def f(root, filename):
    return page_file(root, filename)

run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=True)
