from flask import jsonify

# load modules
from routes.users import users as users_route
from routes.musics import musics as musics_route
from routes.genres import genres as genres_route
from routes.artists import artists as artists_route
from routes.albums import albums as albums_route
from routes.auth import auth as auth_route
from routes.swagger import swagger_ui_blueprint, SWAGGER_URL
from api_spec import spec
from helpers.app import config_app

# configure application and DB
app = config_app()

# register routes
app.register_blueprint(auth_route, url_prefix="/")
app.register_blueprint(users_route, url_prefix="/users")
app.register_blueprint(musics_route, url_prefix="/musics")
app.register_blueprint(genres_route, url_prefix="/genres")
app.register_blueprint(artists_route, url_prefix="/artists")
app.register_blueprint(albums_route, url_prefix="/albums")


# allows to generate Swagger doc for all documented functions
with app.test_request_context():
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


# specify where to get the generated doc
@app.route("/api/swagger.json")
def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())


# register documentation route (see in browser at /api/docs)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# python main entrance program
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=False)
