# -*- coding: utf-8 -*-

"""
## Python package envtools
"""
__version__ = '0.0.0'

import os
from pathlib import Path
import re
from socket import gethostname
import subprocess
from sys import platform # 'linux'|'darwin'|...
from tabulate import tabulate


if not platform in ('linux','darwin'):
    raise NotImplementedError(f"envtools was designed for linux and macos only. Not for {platform=}.")


def get_cluster(unknown_allowed=False) -> str:
    """
    Find out the name of the cluster.

    Returns:
        The name of the cluster. If the cluster is unknown to envtools and unknown_allowed==True, 
        the hostname of the machine is returned, prepended with a '?'.
    
    Raises: 
        NotImplementedError if unknown_allowed==False and the cluster is unknown to envtools.
    """
    try:
        return os.environ['VSC_INSTITUTE_CLUSTER']
    except:
        # not a VSC cluster
        if Path('/appl/lumi').exists():
            return 'lumi'
        # tests for other machines
        else:
            # cluster unknown to envtools: return the hostname prepended with a question mark
            if unknown_allowed: 
                return '?'+gethostname()
            else:
                raise NotImplementedError(f"Cluster unknown to envtools (hostname={gethostname()}).")                                      
    
def has_gpu() -> bool:
    if is_slurm_job():
        return bool(os.environ.get('SLURM_GPUS_ON_NODE',0))
    else:
        raise NotImplementedError("Don't know how to determine the presence of a GPU (except in a SLURM job).")


def get_cpus_per_node() -> int:
    """Return the number of cpus available on a node"""

    if platform == 'darwin':
        output = subprocess.run(['sysctl', 'hw.ncpu'], capture_output=True)
        pattern = re.compile(r'hw\.ncpu: (\d+)\n')
        m = pattern.match(output.stdout.decode('utf-8'))
        return int(m[1])
    elif platform == 'linux':
        output = subprocess.run(['lscpu'], capture_output=True)
        pattern = re.compile(r'CPU\(s\):\s+(\d+)')
        for line in output.stdout.decode('utf-8').splitlines():
            m = pattern.match(line)
            if m:
                return int(m.group(1))
        else:
            raise RuntimeError('Unable to read #cpus/node from lscpu output.')
    else:
        raise NotImplementedError(f"envtools was designed for {platform}.")


# SLURM info
# This is all about accessing environment variables... 
# There are only two reasons to define a convenience function for them:
# - we can come up with a better name that makes the meaning of an environment
#   variable easier to remember
# - the intrinsic type of the environment variable is not a str

def is_slurm_job() -> bool:
    """Return True if the environment is a slurm job"""
    try:
        jobid = os.environ['SLURM_JOBID']
        return True
    except KeyError:
        return False

    
def info():
    """Return a string with all available info from envtools."""
    table = [['platform',platform]]
    try:
        table.append(['cluster',get_cluster()])
        known_cluster = True
    except NotImplementedError:
        table.append(['hostname',gethostname()+" (unknown cluster or stand-alone machine)"])
        known_cluster = False

    if known_cluster and not is_slurm_job():
        table.append(['node', f'login node ({gethostname()})'])

    table.append(['#cpus/node  ', get_cpus_per_node()])
    s = tabulate(table)

    if is_slurm_job():
        s += "\nJob info:\n"
        table = [
             ['job id'        , os.environ['SLURM_JOB_ID']]
            ,['job name'      , os.environ['SLURM_JOB_NAME']]
            ,['partition'     , os.environ['SLURM_JOB_PARTITION']]
            ,['#nodes'        , os.environ['SLURM_JOB_NUM_NODES']]
            ,['#tasks'        , os.environ['SLURM_NTASKS']]
            ,['#cpus per task', os.environ['SLURM_CPUS_PER_TASK']]
            ,['#cpus in job'  , os.environ['SLURM_JOB_CPUS_PER_NODE']]
            ,['#cpus in job'  , os.environ['SLURM_CPUS_ON_NODE']]
            ,['#gpus in job'  , os.environ.get('SLURM_GPUS_ON_NODE',0)]
            ]
        s += tabulate(table)
    
    return s



if __name__ == "__main__":
    print(info())