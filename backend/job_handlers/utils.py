import rq
from rq.job import Job
from typing import Callable

from django.conf import settings

from job_handlers.constants import JobQ
from job_handlers import logger


def enqueue_job(func: Callable, job_q: str = JobQ.DEFAULT_Q, is_async: bool = True, *args, **kwargs) -> Job:
    """
    Enqueue a job to Redis queue.
    """
    if job_q not in JobQ.ALL_QS:
        raise ValueError(f"job_q must be one of {JobQ.ALL_QS}")
    try:
        job = rq.Queue(name=job_q, connection=settings.REDIS_CONN,
                       is_async=is_async).enqueue(func, *args, **kwargs)
    except Exception as ex:
        logger.exception(f"Failed to enqueue job to {job_q} queue")
        raise ex
    return job


def get_job(job_id: str = None, job_q: str = None) -> dict:
    """
    Get details of a job.
    """
    if job_q not in JobQ.ALL_QS:
        raise ValueError(f"job_q must be one of {JobQ.ALL_QS}")
    if job_id is None or job_id == "":
        raise ValueError("job_id must be provided")
    try:
        job = rq.Queue(
            name=job_q, connection=settings.REDIS_CONN).fetch_job(job_id)
    except Exception as ex:
        logger.exception(f"Failed to fetch job {job_id} from {job_q} queue")
        raise ex
    if job is None:
        raise ValueError(f"Job {job_id} not found in {job_q} queue")
    
    return job
