from flask.cli import FlaskGroup, with_appcontext
from flask import current_app
from rq import Connection, Worker

from application import init_app


app = init_app()
cli = FlaskGroup(app)


@cli.command('run_worker')
@with_appcontext
def run_worker():
    with Connection(current_app.redis):
        worker = Worker(["task-queue"])
        with app.app_context():
            worker.work()


if __name__ == '__main__':
    cli()
