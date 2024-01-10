import os

from flask_login import LoginManager

from helpers import db, app
from models.user import User
from schemas.errors import UnauthorizedSchema
from helpers.content_negotiation import content_negotiation


def config_app():
    # db localisation et nom
    uri = 'sqlite:///./users.db'
    app.app_context().push()

    # os.urandom permet de générer un nouveau secret de session (notamment authentification)
    # si vous souhaitez gérer une seule session pour vos tests, remplacez par "secret"
    app.config['SECRET_KEY'] = os.urandom(12)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    login_manager = LoginManager()
    login_manager.init_app(app)

    # Vous pouvez commenter ce callback si vous ne voulez pas de body à vos réponses Unauthorized
    def unauthorized_response():
        error = UnauthorizedSchema().loads("{}")
        return content_negotiation(error, error.get("code"))
    login_manager.unauthorized_callback = unauthorized_response

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
