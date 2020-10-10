import subprocess
import os
import time
import sys


# def run_commands():
#     p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
#     p2 = subprocess.Popen(["grep", "-v", "grep"], stdin=p1.stdout, stdout=subprocess.PIPE)
#     p3 = subprocess.Popen(["grep", "Pages"], stdin=p2.stdout, stdout=subprocess.PIPE)
#     p4 = subprocess.Popen(["tr", "-s", "\" \""], stdin=p3.stdout, stdout=subprocess.PIPE)
#     return p4.communicate()[0].decode('ascii').split(' ')


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
else:
    ps_command = 'Pages'
    timeout = 60*5
print('ps_command: ', ps_command)
print('timeout: ', timeout)


while True:
    header, process_args = run_ps_commands(ps_command)
    if not process_args:
        time.sleep(timeout)
        continue
    print(process_args)
    cpu_time_arg_index = header.index('TIME')
    cpu_start = process_args[cpu_time_arg_index]
    print('cpu_start: ' + cpu_start)
    time.sleep(timeout)
    header, process_args = run_ps_commands(ps_command)
    print(process_args)
    if not process_args:
        continue
    cpu_end = process_args[cpu_time_arg_index]
    print('cpu_end: ' + cpu_end)
    if cpu_end == cpu_start:
        pid_arg_index = header.index('PID')
        pid = process_args[pid_arg_index]
        print(pid)
        os.system('kill ' + pid)


# process_args = run_ps_commands('Pages')
# print(process_args)
# exit()



# timeout = 30
# interval = 5
# while True:
#     count = 0
#     for i in range(interval):
#         time.sleep(1)
#         result = run_commands()
#         print(result)
#         if len(result) > 1:
#             cpu = result[2]
#             print(cpu)
#             if float(cpu) == 0.0:
#                 count += 1
#             else:
#                 break;
#     if count == interval:
#         pid = result[1]
#         print(pid)
#         os.system('kill ' + pid)
#     time.sleep(timeout)



# timeout = 60
# while True:
#     result = run_commands()
#     print(result)
#     time.sleep(timeout)



# timeout = 60*5
# while True:
#     result = run_commands()
#     print(result)
#     if len(result) < 2:
#         time.sleep(timeout)
#         continue
#     cpu_start = result[2]
#     print(cpu_start)
#     time.sleep(timeout)
#     result = run_commands()
#     print(result)
#     if len(result) < 2:
#         continue
#     cpu_end = result[2]
#     print(cpu_end)
#     if cpu_end == cpu_start:
#         pid = result[1]
#         print(pid)
#         os.system('kill ' + pid)

