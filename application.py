from flask import Flask, render_template
from restapi import restapi_blueprint
import logging

application = Flask(__name__)
application.register_blueprint(restapi_blueprint, url_prefix="/restapi")


@application.route('/service')
def service():
    return render_template(
        'service.html'
    )


@application.route('/')
def index():
    return render_template(
        'index.html'
    )


if __name__ == '__main__':
    logging.info("Flask web server started!")

    application.debug = True
    application.run(host="localhost", port="8080")
