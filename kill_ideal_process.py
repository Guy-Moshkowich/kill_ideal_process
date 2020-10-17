import subprocess
import os
import time
import sys
import logging


def run_ps_commands(command):
    ps_result = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    lines = ps_result.split('\n')
    header = lines[0].split()
    command_arg_index = header.index('COMMAND')
    for i in range(1, len(lines)):
        process_args = lines[i].split()
        if len(process_args) < command_arg_index:
            continue
        command_arg = process_args[command_arg_index]
        if command in command_arg:
            return header, process_args
    return [], []


if len(sys.argv) > 1:
    ps_command = sys.argv[1]
    timeout = int(sys.argv[2])


while True:
    header, process_args = run_ps_commands(ps_command)
    if not process_args:
        time.sleep(timeout)
        continue
    logging.debug(process_args)
    cpu_time_arg_index = header.index('TIME')
    cpu_start = process_args[cpu_time_arg_index]
    logging.debug('cpu_start: ' + cpu_start)
    time.sleep(timeout)
    header, process_args = run_ps_commands(ps_command)
    logging.debug(process_args)
    if not process_args:
        continue
    cpu_end = process_args[cpu_time_arg_index]
    logging.debug('cpu_end: ' + cpu_end)
    if cpu_end == cpu_start:
        pid_arg_index = header.index('PID')
        pid = process_args[pid_arg_index]
        logging.debug(pid)
        os.system('kill ' + pid)
