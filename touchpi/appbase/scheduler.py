from touchpi.common.config import scheduler
from datetime import datetime, timedelta
from time import sleep


def add_onetime_job(*args, **kwargs):
    job = scheduler.add_job(*args, 'date', **kwargs)
    sleep(0.01)
    return job.id


def add_onetime_job_now(*args, **kwargs):
    job = scheduler.add_job(*args, 'date', **kwargs, next_run_time=datetime.now(), misfire_grace_time=None)
    sleep(0.01)
    return job.id


def add_interval_job(*args, **kwargs):
    job = scheduler.add_job(*args, 'interval', **kwargs)
    sleep(0.01)
    return job.id


def add_interval_job_now(*args, **kwargs):
    job = scheduler.add_job(*args, 'interval', **kwargs, next_run_time=datetime.now(), misfire_grace_time=None)
    sleep(0.01)
    return job.id


def remove_job(job_id):
    if get_job(job_id) is not None:
        scheduler.remove_job(job_id)


def pause_job(job_id):
    if get_job(job_id) is not None:
        scheduler.pause_job(job_id)


def resume_job(job_id):
    if get_job(job_id) is not None:
        scheduler.resume_job(job_id)


def modify_job(job_id, *args, **kwargs):
    if get_job(job_id) is not None:
        scheduler.modify_job(*args, **kwargs, job_id=job_id)


def get_job(job_id):
    return scheduler.get_job(job_id)


def next_run_time_in_seconds(second):
    return datetime.now() + timedelta(seconds=second)
