from celery import Celery


def make_celery(app):
    """Initialize celery application with configurations from src.config.flask_config

    Args:
        app: flask application

    Returns:
        class: celery application

    """
    celery = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery
