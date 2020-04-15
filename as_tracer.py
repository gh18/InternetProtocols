import subprocess
import re
from urllib import request
import sys
import json
import os.path
import datetime


# constants to simplify further code
save_path = '/Users/miha/Desktop/logs/'
filename = 'logs_' + str(format(datetime.datetime.now(), '%Y-%m-%d_%H.%M.%S'))
help_args = {'--help', '-h', '-help'}
help_message = """
    Traces routes to specified nodes
    Shows Autonomous System (AS) info of traced nodes
    USAGE: python as_tracker.py [IP_Address_Or_Domain_Name]
    Example: python as_tracer.py example.com"""


if len(sys.argv) != 2:
    print(help_message)
    sys.exit()
if sys.argv[1] in help_args:
    print(help_message)
    sys.exit()
else:
    _ip = sys.argv[1]

# calling the shell and passing the command with args
try:
    trace_route = subprocess.check_output('traceroute -a ' + _ip, shell=True).decode('utf-8')
    with open(os.path.join(save_path, filename + '.txt'), 'w') as file:
        for line in trace_route:
            # trying to get rid off Timeout Requests in log_file
            if '*' not in line:
                file.writelines(line)
            else:
                continue
except subprocess.CalledProcessError as ex:
    print('Something went wrong: Check or Internet connection or contact your Provider')
    sys.exit()


# using free Internet sources to get JSON-information about ip_addresses
def get_ip_info(ip_address):
    return json.loads(request.urlopen('http://ip-api.com/json/' + ip_address).read())


# first entry is local router (at least when using Wi-Fi)
output_parsed = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", trace_route)[1:]
# as_parsed = re.match(r'^ASd+$', trace_route)[1:]


def print_out_info(parsed_data: list):
    print_out_list = list()
    for ip_addr in parsed_data:
        info = get_ip_info(ip_addr)
        if info['status'] == 'success':
            print_out_list.append(str(len(print_out_list) + 1) + '\t'
                                  + ip_addr + '\t'
                                  + info['as'].split(' ')[0] + '\t'           # TODO: fix this
                                  + info['country'] + '\t'
                                  + info['isp'])

    for entry in print_out_list:
        print(entry)


print_out_info(output_parsed)
