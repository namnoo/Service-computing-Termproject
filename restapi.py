from flask import Blueprint, render_template

restapi_blueprint = Blueprint('restapi', __name__)


@restapi_blueprint.route('/execute')
def restapi_execute():
    return render_template(
        'restapi_execute.html'
    )


@restapi_blueprint.route('/reference')
def restapi_documentation():
    return render_template(
        'restapi_reference.html'
    )
