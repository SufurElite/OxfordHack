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
from appGen import QuestionGenerator
from connect_database import uploadQAs, downloadQAs, getStudySets
import pprint
import random 

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
    pp = pprint.PrettyPrinter(indent=4)
    random.seed(42)
    data = [s.strip() for s in text.splitlines()]
    print(len(data))
    pp = pprint.PrettyPrinter(indent=4)
    QAs = []
    for i in data:
      if len(i)>50:
        try:
          qg = QuestionGenerator(i)
          questions = qg.process(top_sentences=2)
          #print(i)
          for q in questions:
            #pp.pprint(q)
            qa = (q['question_gap'],q['answer'])
            QAs.append(qa)
            #input(qa)
          #input()
        except Exception as e:
          #print("Error encountered, but let's keep trying" + str(e))
          print()
    res = {
      "success": True,
      "QAs": QAs
    }
    #input(QAs)
    uploadQAs(args["email"],args["setname"],QAs)
    return res


class getCards(Resource):
  def post(self):
    args = parser.parse_args()
    print(args)
    cards = downloadQAs(args["email"], args["setname"])
    res = {
      "success": True,
      "cards": cards
    }
    return res

class getSets(Resource):
  def post(self):
    args = parser.parse_args()
    print(args)
    studysets = getStudySets(args["email"])
    res = {
      "success": True,
      "sets": studysets
    }
    return res

api.add_resource(parseText, "/parse/")
api.add_resource(getCards, "/getCards/")
api.add_resource(getSets, "/getSets/")
if __name__ == "__main__":
  app.run(debug=False, threaded=False)
