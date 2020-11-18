import subprocess
import os
import time
import sys
import logging
from logging.handlers import RotatingFileHandler


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


log_level = logging.INFO
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
handler = RotatingFileHandler('killer_ideal_process.log', maxBytes=100000, backupCount=5)
handler.setFormatter(formatter)
logger = logging.getLogger("Rotating Log")
logger.addHandler(handler)

if len(sys.argv) > 1:
    ps_command = sys.argv[1]
    timeout = int(sys.argv[2])
    log_level_str = sys.argv[3]
    if log_level_str == 'debug':
        log_level = logging.DEBUG
        logger.setLevel(log_level)

# logging.basicConfig(filename='myapp.log', level=log_level)
logger.info('Started')
logger.info('ps_command:' + ps_command)
logger.info('timeout: ' + str(timeout))


while True:
    header, process_args = run_ps_commands(ps_command)
    if not process_args:
        time.sleep(timeout)
        continue
        logger.debug(process_args)
    cpu_time_arg_index = header.index('TIME')
    cpu_start = process_args[cpu_time_arg_index]
    logger.debug('cpu_start: ' + cpu_start)
    time.sleep(timeout)
    header, process_args = run_ps_commands(ps_command)
    logger.debug(process_args)
    if not process_args:
        continue
    cpu_end = process_args[cpu_time_arg_index]
    logger.debug('cpu_end: ' + cpu_end)
    if cpu_end == cpu_start:
        pid_arg_index = header.index('PID')
        pid = process_args[pid_arg_index]
        logger.debug('try to kill process: ' + pid)
        os.system('kill -9 ' + pid)
    else:
        logger.debug('there is delta.')
