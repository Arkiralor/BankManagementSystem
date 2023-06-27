import rq
from rq.job import Job
from typing import Callable

from django.conf import settings

from job_handlers.constants import JobQ
from job_handlers import logger

def enqueue_job(func: Callable, job_q: str = JobQ.DEFAULT_Q, is_async:bool = True, *args, **kwargs) -> Job:
    """
    Enqueue a job to Redis queue.
    """
    if job_q not in JobQ.ALL_QS:
        raise ValueError(f"job_q must be one of {JobQ.ALL_QS}")

    job = rq.Queue(name=job_q, connection=settings.REDIS_CONN, is_async=is_async).enqueue(func, *args, **kwargs)
    return job