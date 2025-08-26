# -*- coding: utf-8 -*-

"""
## Python package envtools
"""
__version__ = '0.0.0'

import os
from pathlib import Path
import re
import subprocess
from sys import platform # 'linux'|'darwin'|...
from tabulate import tabulate


if not platform in ('linux','darwin'):
    raise NotImplementedError(f"envtools was designed for linux and macos only. Not for {platform}.")


def get_cluster():
    """Return the lowercase name of the cluster """
    try:
        cluster = os.environ['VSC_INSTITUTE_CLUSTER']
    except:
        if Path('/appl/lumi').exists():
            cluster = 'lumi'
        # tests for other machines
        else:
            raise NotImplementedError('get_cluster(): Unable to find out which cluster we are running on.')
                                      
    return cluster



def get_cpus_per_node() -> int:
    """Return the number of cpus available on a node"""

    if platform == 'darwin':
        output = subprocess.run(['sysctl', 'hw.ncpu'], capture_output=True)
        pattern = re.compile(r'hw\.ncpu: (\d+)\n')
        m = pattern.match(output.stdout.decode('utf-8'))
        return int(m[1])
    elif platform == 'linux':
        if is_slurm_job():
            return int(os.environ['SLURM_CPUS_ON_NODE'])
        else:
            output = subprocess.run(['lscpu'], capture_output=True)
            pattern = re.compile(r'CPU(s):\s+(\d+)\n')
            for line in output.stdout.decode('utf-8').splitlines():
                m = pattern.match(line)
                if m:
                    return int(m.group(1))
    else:
        raise NotImplementedError(f"envtools was designed for {platform}.")


# SLURM info
def is_slurm_job() -> bool:
    """Return True if the environment is a slurm job"""
    try:
        jobid = os.environ['SLURM_JOBID']
        return True
    except KeyError:
        return False

def get_partition():
    """Get the partition on which we are running. The empty string identifies a login node."""
    return os.environ.get('SLURM_JOB_PARTITION', default='')

def get_job_cpus() -> int:
    """Return the number of cpus available to the job."""
    return os.environ.get('SLURM_JOB_CPUS_PER_NODE')


def info():
    """Return a string with all available info from envtools."""
    table = [['platform',platform]
            ,['cluster',get_cluster()]
            ]

    partition = get_partition()
    if not partition:
        table.append(['node', 'login node or stand-alone'])
    else:
        table.append(['partition', partition])

    table.append(['#cpus', get_cpus_per_node()])

    return tabulate(table)



if __name__ == "__main__":
    print(info())