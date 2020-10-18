from flask import redirect, Blueprint, url_for

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return redirect(url_for('auth.login'))
