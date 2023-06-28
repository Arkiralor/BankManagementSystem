"""
Initialize the logger for the application.
"""
import logging

logger = logging.getLogger('logger.' + __name__)
default_app_config = 'experiments_app.apps.ExperimentsAppConfig'