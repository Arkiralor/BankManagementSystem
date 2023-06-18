"""
Initialize the logger for the application.
"""
import logging

logger = logging.getLogger('logger.' + __name__)
default_app_config = 'ledger_app.apps.LedgerAppConfig'