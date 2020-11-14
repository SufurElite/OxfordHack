from flask import Flask, render_template, request 
import numpy as np
import re, sys, os 
from load import *
from flask_cors import CORS

# ./python_code/api.py
import os
import pickle
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
# initialise flask app


app = Flask(__name__)
CORS(app)
api = Api(app)

# Require a parser to parse our POST request.
parser = reqparse.RequestParser()



class Temp(Resource):
  def post(self):
    args = parser.parse_args()
    
    return res


api.add_resource(Temp, "/temp")
if __name__ == "__main__":
  app.run(debug=False, threaded=False)