"""
Module to handle Redis job queue.
"""

import logging
from redis import Redis

from django.conf import settings

logger = logging.getLogger('logger.' + __name__)

# REDIS_CONN = Redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")

