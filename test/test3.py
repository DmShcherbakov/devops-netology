#!/usr/bin/env python3

import dns.resolver

prev_check_file = './prev.chck'
addr_dict_old = {}
addr_dict_new = {}
addr_list = ['drive.google.com', 'mail.google.com', 'google.com']

with open(prev_check_file, 'r') as fread:
    for rstr in fread:
        key, value = rstr.split(': ')
        value = value.replace('\n','')
#        addr_dict_old.update({key:value})
        addr_dict_old[key] = value

with open(prev_check_file, 'w') as f:
    f.close

for addr in addr_list:
    answer = dns.resolver.query(addr, 'A')
    ip_a = answer[0].to_text()
    print(addr, '-', ip_a)
    addr_dict_new[f'{addr}'] = ip_a

with open(prev_check_file, 'a') as f:
        for key, value in  addr_dict_new.items():
            f.write(f'{key}: {value}\n')

for  key, value in addr_dict_new.items():
    if addr_dict_new.get(key) != addr_dict_old.get(key):
        print(f'[ERROR] {key} IP mismatch: {addr_dict_old.get(key)} {addr_dict_new.get(key)}')
