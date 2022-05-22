
from queue import Empty
from flask import Blueprint, jsonify, request, make_response
from app.utils.loadfiles import LoadFiles
import os
from app.models.response import response
import json

loadfile = LoadFiles()
serviceFile = Blueprint("serviceFile", __name__)

servicename = '/storage'


@serviceFile.route('/')
def index():
    config = getconfig('config')
    datatable = loadfile.getData(config=config)
    result = datatable.to_json(orient="records")
    parsed = json.loads(result)
    res = response(data=json.dumps(parsed, indent=4))
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
        dirFiles = dirFiles + '/'
        data = {
            'xlsm': dirFiles + files[0],
            'txt': dirFiles + files[1]
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
