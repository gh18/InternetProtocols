# import sys
# import pickle
# import subprocess
#
# ip = input()
# url = 'https://www.nic.ru/whois/?searchWord=' + ip + '/json'
# try:
#     trace = subprocess.check_output('traceroute ' + ip, shell=True).decode('utf-8')
# except subprocess.CalledProcessError:
#     print('Error!')
#     sys.exit()
#
# json_info = str(pickle.loads(url))
# print(json_info)
import re


it = '91.291.149.1'
output_parsed = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", it)
print(output_parsed)
