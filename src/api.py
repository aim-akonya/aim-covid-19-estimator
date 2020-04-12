from flask import Flask, jsonify, request, Response, g
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import dicttoxml
import estimator
import time;

application = Flask(__name__)
application.logger_name = "covid19.app"
application.config['DEBUG'] = True
application.config['SECRET_KEY'] = 'Pn327@ms9oY-L5'
CORS(application)

#start timer
@application.before_request
def start_timer():
    g.start = time.time()

@application.route("/api/v1/on-covid-19", methods=["GET","POST"])
def get_on_covid_19():
    try:
        output = estimator.estimator(request.get_json())
    except:
        return Response({"message":"An Error Occured"}), 400
    
    return jsonify(output), 200


@application.route("/api/v1/on-covid-19/json", methods=["POST"])
def get_json_covid_19_():
    try:
        output = estimator.estimator(request.get_json())
    except:
        return Response({"message":"An Error Occured"}), 400
    return jsonify(output), 200

@application.route("/api/v1/on-covid-19/xml", methods=["POST"])
def get_xml_covid_19_():
    try:
        output = estimator.estimator(request.get_json())
    except:
        return Response({"message":"An Error Occured"}), 400
    
    xml_format = dicttoxml.dicttoxml(output, attr_type=False, custom_root='impactEstimation')
    return Response(xml_format, mimetype="text/xml")


@application.route("/api/v1/on-covid-19/logs", methods=["POST"])
def get_logs_covid_19_():
    f= open("./app.log", "r")
    file_list = f.readlines()
    f.close()
    return Response(file_list, mimetype="text/data"), 200

@application.teardown_request
def after_request_func(err):
    method = request.method
    path =  request.path
    now = time.time()
    duration = round(now - g.start, 2)
    if (err != None):
        status = 400
    else:
        status = 200
        
    application.logger.info(f'{method}\t\t{path}\t\t{status}\t\t{duration} ms')


if (__name__=="__main__"):
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.run(port="5000")
