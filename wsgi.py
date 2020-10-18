#!/user/bin/env python
import click

from app import create_app, db, models, forms
from app.models import Client, User
from tests import test_app

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    default_client = Client(fullname="Клиент", phone=89100000000)
    default_client.save()
    user = User(username='admin', password=)
    user.save()
    


@app.cli.command()
@click.confirmation_option(prompt='Drop all database tables?')
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == '__main__':
    app.run()
