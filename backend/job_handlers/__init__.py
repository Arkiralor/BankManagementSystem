"""
Module to handle Redis job queue.
"""
from os import path
import logging

from django.conf import settings

logger = logging.getLogger('logger.' + __name__)
redis_logger = logging.getLogger('mslate_logger.redis')
redis_logger.addHandler(logging.FileHandler(path.join(settings.LOG_DIR, 'redis.log')))

