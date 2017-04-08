from bottle import *
import os

def page_file(root, filename):
    return static_file(filename, root=root)

@get("/")
def man():
    return static_file("index.html", root=".")

@route("/<root>/<filename>")
def f(root, filename):
    return page_file(root, filename)

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
