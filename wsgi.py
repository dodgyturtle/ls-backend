#!/user/bin/env python
import click

from app import create_app, db, models, forms
from app.models import Client, User
from tests import test_app

application = create_app()


# flask cli context setup
@application.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(application=application, db=db, models=models, forms=forms)


@application.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    default_client = Client(fullname="Клиент", phone=89100000000)
    default_client.save()
    user = User(username="admin", password="123")
    user.save()


@application.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    application.run()
