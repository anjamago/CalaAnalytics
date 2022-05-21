
from queue import Empty
from flask import Blueprint, jsonify, request, make_response
from app.utils.loadfiles import LoadFiles
import os
from app.models.response import response
loadfile = LoadFiles()
serviceFile = Blueprint("serviceFile", __name__)

servicename = '/storage'


@serviceFile.route('/')
def index():
    loadfile.getTxt()
    return "hi"


@serviceFile.route('/location')
def method_name():
    erros = {}
    dirFiles = getconfig('config', 'blob')
    filesList = getconfig('config', 'filesnames')

    if dirFiles is None or dirFiles is Empty:
        erros["dir"] = "file directory does not exist"

    if filesList is None or filesList is Empty:
        erros["dir"] = "error loading files"

    if not erros:
        dirFiles = dirFiles + '/'
        data = {
            'xlsm': dirFiles + filesList[0],
            'txt': dirFiles + filesList[1]
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


def getconfig(key, property):
    yamlfile = os.path.abspath('config.yaml')
    data = loadfile.getYaml(yamlfile)
    element = data.get(key)
    return element.get(property)
