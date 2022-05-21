from flask import Flask, jsonify, request
from app.services.serviceFile import serviceFile, servicename


versionApi = '/v1'
app = Flask(__name__)
app.register_blueprint(serviceFile, url_prefix=versionApi+servicename)


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': "hola mundo"
    })


if __name__ == "__main__":
    app.run(debug=True)
