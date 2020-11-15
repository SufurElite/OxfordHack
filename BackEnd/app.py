from flask import Flask, render_template, request 
import numpy as np
import re, sys, os 
from load import *
from flask_cors import CORS
from getText import loadPdfText, loadImageText
# ./python_code/api.py
import os
import pickle
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
import numpy as np

# initialise flask app
app = Flask(__name__)
CORS(app)
api = Api(app)

# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
""""setname" : this.flashSetName, "subject" : this.Subject, "email": this.email, "fileID":dest"""
parser.add_argument("setname")
parser.add_argument("subject")
parser.add_argument("email")
parser.add_argument("fileID")


class parseText(Resource):
  def post(self):
    args = parser.parse_args()
    print(args)
    if args["fileID"][0]=="i":
      text = loadImageText(args["fileID"])
    elif args["fileID"][0]=="F":
      text = loadPdfText(args["fileID"])
    res = {
      "txt": text
    }
    return res


api.add_resource(parseText, "/parse/")
if __name__ == "__main__":
  app.run(debug=False, threaded=False)
