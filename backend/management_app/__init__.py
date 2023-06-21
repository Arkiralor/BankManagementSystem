"""
Django application to hold all the management related functionality.
"""
import logging

default_app_config = 'management_app.apps.ManagementAppConfig'
logger = logging.getLogger('logger.' + __name__)