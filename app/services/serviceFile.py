
from queue import Empty
from flask import Blueprint, jsonify, request, make_response
from pandas import date_range
from app.utils.loadfiles import LoadFiles
import os
from app.models.response import response
import json
from flask_cors import CORS


loadfile = LoadFiles()
serviceFile = Blueprint("serviceFile", __name__)
CORS(serviceFile)
servicename = '/storage'


@serviceFile.route('/')
def index():
    config = getconfig('config')
    datatable = loadfile.getData(config=config)
    result = datatable.to_json(orient="records")
    parsed = json.loads(result)
    res = response(data=parsed)
    return make_response(
        jsonify(res),
        res['status']
    )


@serviceFile.route('/chart')
def chart():
    config = getconfig('config')
    datatable = loadfile.getData(config=config)

    datatable.drop_duplicates(['Tipo de pedido'])

    data = datatable.drop(
        columns=["Nombre", "Apellido", "Cedula", "Nacimiento", "Edad"])
    cliente = datatable.drop_duplicates(['Nombre Completo'])
    data_response = {}
    for key in cliente['Nombre Completo']:
        produts = data.where(data['Nombre Completo'] == key).dropna().drop(
            columns=['Nombre Completo'])
        datajson = produts.to_json(orient="records")
        productos = {}
        for item in json.loads(datajson):
            productos[item['Tipo de pedido']] = item['Numero de pedido']

        data_response[key] = productos

    res = response(data=data_response)
    return make_response(
        jsonify(res),
        res['status']
    )


@serviceFile.route('/location')
def method_name():
    erros = {}
    dir_blob = getconfig('config', 'blob')
    files = getconfig('config', 'filesnames')

    if dir_blob is None or dir_blob is Empty:
        erros["dir"] = "file directory does not exist"

    if files is None or files is Empty:
        erros["dir"] = "error loading files"

    if not erros:
        dir_blob = dir_blob + '/'
        data = {
            'xlsm': dir_blob + files[0],
            'txt': dir_blob + files[1]
        }

        res = response(data=data)

        return make_response(
            jsonify(res),
            res['status']
        )
    res = response(status=404, data=erros, message="Errors")
    return make_response(
        jsonify(res),
        res['status']
    )


def getconfig(key, property=None):
    yamlfile = os.path.abspath('config.yaml')
    data = loadfile.getYaml(yamlfile)
    element = data.get(key)
    if property is None:
        return element
    return element.get(property)
