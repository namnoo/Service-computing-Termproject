from flask import Blueprint, render_template
from hospital_clinic_Info import hospital_clinic_DB
from medical_examination import medical_examination_search_module
from children_hospital import children_hospital_search_module
from pharmacy_Info import pharmacy_store_DB


restapi_blueprint = Blueprint('api', __name__)


@restapi_blueprint.route('/')
def restapi_execute():

    return render_template(
        'restapi_execute.html'
    )


@restapi_blueprint.route('/hospital/<sido>/<gu>')
def restapi_execute_hospital(sido, gu):
    data = hospital_clinic_DB.search_hostpital_city(sido, gu)

    return render_template(
        'restapi_execute.html', hospital=data
    )


@restapi_blueprint.route('/clinic/<sido>/<gu>')
def restapi_execute_clinic(sido, gu):
    data = hospital_clinic_DB.search_clinic_city(sido, gu)

    return render_template(
        'restapi_execute.html', clinic=data
    )


@restapi_blueprint.route('/examination/<sido>/<gu>')
def restapi_execute_examination(sido, gu):
    data = medical_examination_search_module.citySearch(sido, gu)

    return render_template(
        'restapi_execute.html', examination=data
    )


@restapi_blueprint.route('/children/<sido>/<gu>')
def restapi_execute_children(sido, gu):
    data = children_hospital_search_module.citySearch(sido, gu)

    return render_template(
        'restapi_execute.html', children=data
    )


@restapi_blueprint.route('/pharmacy/<sido>/<gu>')
def restapi_execute_pharmacy(sido, gu):
    data = pharmacy_store_DB.search_pharmacy_city(sido, gu)

    return render_template(
        'restapi_execute.html', pharmacy=data
    )


@restapi_blueprint.route('/store/<sido>/<gu>')
def restapi_execute_store(sido, gu):
    data = pharmacy_store_DB.search_store_city(sido, gu)

    return render_template(
        'restapi_execute.html', store=data
    )


@restapi_blueprint.route('/reference')
def restapi_documentation():
    return render_template(
        'restapi_reference.html'
    )