#!flask/bin/python
import sqlite3
from flask import Flask, jsonify, abort, request, make_response, url_for, g
from flask.ext.httpauth import HTTPBasicAuth
app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()
DATABASE = './rice.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@auth.get_password
def get_password(username):
    if username == 'logos':
        return 'linux'
    return None
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the
    # default auth dialog
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
packages = [{
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
    "description": "test.",
    "url": "http://bwasti.com:9001/test.zip",
    "images": ["http://bwasti.com:9001/test3.png"]
}
]
def make_public_package(package):
    new_package = {}
    for field in package:
        if field == 'id':
            new_package['uri'] = url_for(
                'get_package', package_id=package['id'], _external=True)
        else:
            new_package[field] = package[field]
    return new_package
@app.route('/ricedb/api/v1.0/packages', methods=['GET'])
def get_packages():
    # map(make_public_package, packages) } )
    return jsonify({'packages': [dict(zip(['id','title','program','url','images','description'],pkg)) for pkg in list(get_db().execute('SELECT * FROM packages'))]}) #this is horrible
@app.route('/ricedb/api/v1.0/packages/<int:package_id>', methods=['GET'])
def get_package(package_id):
    package = [dict(zip(['id','title','program','url','images','description'],pkg)) for pkg in list(get_db().execute('SELECT * FROM packages WHERE id=%d'%package_id))]
    if len(package) == 0:
        abort(404)
    return jsonify({'package': make_public_package(package[0])})
@app.route('/ricedb/api/v1.0/packages', methods=['POST'])
@auth.login_required
def create_package():
    if not request.json or not 'title' in request.json:
        abort(400)
    package = {
        'title': request.json['title'],
        'program': request.json['program'],
        'url': request.json['url'],
        'images': request.json['images'],
        'description': request.json.get('description', ""),
    }
    with app.app_context():
        db = get_db()
        db.cursor().execute("INSERT INTO packages VALUES (null, '{title}', '{program}', '{url}', \"{images}\", \"{description}\")".format(**package))#TODO:sql injection
        db.commit()
    return jsonify({'package': make_public_package(package)}), 201
@app.route('/ricedb/api/v1.0/packages/<int:package_id>', methods=['PUT'])
@auth.login_required
def update_package(package_id):
    package = [dict(zip(['id','title','program','url','images','description'],pkg)) for pkg in list(get_db().execute('SELECT * FROM packages WHERE id=%d'%package_id))]
    if len(package) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    package[0]['title'] = request.json.get('title', package[0]['title'])
    package[0]['description'] = request.json.get(
        'description', package[0]['description'])
    package[0]['program'] = request.json.get('program', package[0]['program'])
    package[0]['url'] = request.json.get('url', package[0]['url'])
    package[0]['images'] = request.json.get('images', package[0]['images'])
    package[0]['id'] = package_id
    with app.app_context():
        db = get_db()
        db.cursor().execute("UPDATE packages SET ('{title}', '{program}', '{url}', \"{images}\", \"{description}\") WHERE id={id}".format(**package[0])) #untested
        db.commit()
    
    return jsonify({'package': make_public_package(package[0])})
@app.route('/ricedb/api/v1.0/packages/<int:package_id>', methods=['DELETE'])
@auth.login_required
def delete_package(package_id):
    package = [dict(zip(['id','title','program','url','images','description'],pkg)) for pkg in list(get_db().execute('SELECT * FROM packages WHERE id=%d'%package_id))]
    if len(package) == 0:
        abort(404)
    with app.app_context():
        db = get_db()
        db.cursor().execute("DELETE from packages WHERE id="+package_id) #untested
        db.commit()
    return jsonify({'result': True})

def init_db():
    '''import the schema. ***damn pain in the ass to write'''
    with app.app_context():
        db = get_db()
        with open('schema.sql', mode='r') as f:
            db.executescript(f.read())
        for pkg in packages:
            print(pkg)
            db.cursor().execute("INSERT INTO packages VALUES (null, '{title}', '{program}', '{url}', \"{images}\", \"{description}\")".format(**pkg))
        db.commit()


if __name__ == '__main__':
    app.run(debug=True)
