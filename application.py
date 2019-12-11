from flask import Flask, render_template
from restapi import restapi_blueprint
import logging, json

application = Flask(__name__)
application.register_blueprint(restapi_blueprint, url_prefix="/api")


@application.route('/service')
def service():
    with open('administrative_district.json', encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    return render_template(
        'service.html', sido=json_data["data"]
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
