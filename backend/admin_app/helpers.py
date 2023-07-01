from datetime import datetime
from os import environ

from rest_framework import status

from core.boilerplate.response_template import Resp

from psutil import virtual_memory, cpu_percent, cpu_count, disk_usage, net_io_counters, Process, AccessDenied, NoSuchProcess, \
    disk_partitions, disk_io_counters, sensors_temperatures, sensors_fans, sensors_battery, boot_time, users, pids

from admin_app import logger
    

class SystemInfoAPIHelpers:

    @classmethod
    def get_hw_info(cls):
        resp = Resp()

        data = {
            "cpu_count": cpu_count(),
            "cpu_percent": cpu_percent(),
            "virtual_memory": virtual_memory(),
            "disk_usage": disk_usage("/"),
            "disk_partitions": disk_partitions(),
            "disk_io_counters": disk_io_counters(),
            "net_io_counters": net_io_counters(),
            "sensors_temperatures": sensors_temperatures(),
            "sensors_fans": sensors_fans(),
            "sensors_battery": sensors_battery(),
            "boot_time": boot_time(),
            "users": users(),
            "pids": pids(),
            "evironment": environ
        }

        resp.message = "System Info"
        resp.data = data
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp
