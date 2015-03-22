#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'logos':
        return 'linux'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

packages =  [ {
"id": 1,
"title": "linux repo 1",
"program": "i3",
"description": "This is a sample of the description field.",
"url": "http://bwasti.com:9001/test.zip",
"images": ["http://bwasti.com:9001/test.jpg"]
},
{
"id": 2,
"title": "linux repo 2",
"program": "i3",
"description": "Does this description thing work?.",
"url": "http://bwasti.com:9001/test.zip",
"images": ["http://bwasti.com:9001/test2.jpg"]
},
{
"id": 3,
"title": "linux repo 3",
"program": "i3",
"Description": "test.",
"url": "http://bwasti.com:9001/test.zip",
"images": ["http://bwasti.com:9001/test3.png"]
}
]


def make_public_package(package):
    new_package = {}
    for field in package:
        if field == 'id':
            new_package['uri'] = url_for('get_package', package_id = package['id'], _external = True)
        else:
            new_package[field] = package[field]
    return new_package
    
@app.route('/ricedb/api/v1.0/packages', methods = ['GET'])
def get_packages():
    return jsonify( { 'packages': packages })#map(make_public_package, packages) } )

@app.route('/ricedb/api/v1.0/packages/<int:package_id>', methods = ['GET'])
def get_package(package_id):
    package = list ( filter(lambda t: t['id'] == package_id , packages) )
    if len(package) == 0:
        abort(404)
    return jsonify( { 'package': make_public_package(package[0]) } )

@app.route('/ricedb/api/v1.0/packages', methods = ['POST'])
@auth.login_required
def create_package():
    if not request.json or not 'title' in request.json:
        abort(400)
    package = {
        'id': packages[-1]['id'] + 1,
        'title': request.json['title'],
        'program': request.json['program'],
        'url': request.json['url'],
        'images': request.json['images'],
        'description': request.json.get('description', ""),
    }
    packages.append(package)
    return jsonify( { 'package': make_public_package(package) } ), 201

@app.route('/ricedb/api/v1.0/packages/<int:package_id>', methods = ['PUT'])
@auth.login_required
def update_package(package_id):
    package = list(filter(lambda t: t['id'] == package_id, packages))
    if len(package) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    package[0]['title'] = request.json.get('title', package[0]['title'])
    package[0]['description'] = request.json.get('description', package[0]['description'])
    package[0]['program'] = request.json.get('program', package[0]['program'])
    package[0]['url'] = request.json.get('url', package[0]['url'])
    package[0]['images'] = request.json.get('images', package[0]['images'])
    return jsonify( { 'package': make_public_package(package[0]) } )
    
@app.route('/ricedb/api/v1.0/packages/<int:package_id>', methods = ['DELETE'])
@auth.login_required
def delete_package(package_id):
    package = list(filter(lambda t: t['id'] == package_id, packages) )
    if len(package) == 0:
        abort(404)
    packages.remove(package[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)
