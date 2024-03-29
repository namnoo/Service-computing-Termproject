from flask import Flask, render_template, request
from restapi import restapi_blueprint
from keys import KAKAO_MAP
import logging, json

application = Flask(__name__)
application.register_blueprint(restapi_blueprint, url_prefix="/api")


@application.route('/service', methods=['POST','GET'])
def service():
    with open('administrative_district.json', encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    result = ''
    if request.method == 'POST':
        result = request.form

    return render_template('service.html', result=result, sido=json_data["data"])


@application.route('/servlce', methods=['POST','GET'])
def service_result():
    with open('administrative_district.json', encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    result = ''
    if request.method == 'POST':
        result = request.form

    return render_template('result.html', result=result, sido=json_data["data"])


@application.route('/service/map/<name>/<address>')
def map(name, address):

    return render_template(
        'map.html', key=KAKAO_MAP, name=name, address=address
    )


@application.route('/')
def index():
    return render_template(
        'index.html'
    )


if __name__ == '__main__':
    logging.info("Flask web server started!")

    application.debug = True
    application.run(host="0.0.0.0", port="8080")

