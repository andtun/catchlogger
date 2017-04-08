from bottle import *
import os

def page_file(filename):
    return static_file(filename, root='pagefiles/')

@get("/")
def man():
    return static_file("Parallax Template - Materialize.html", root=".")

@route("/returnfile/<filename>")
def f(filename):
    return page_file(filename)

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
