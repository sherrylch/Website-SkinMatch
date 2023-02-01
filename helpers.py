import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session



# Display an error message
def error(message):
       def replace(m):
              m = m.replace(message, message)
              return m
       return render_template("error.html", message=replace(message))





