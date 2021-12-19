#!/usr/bin/env python3

import dns.resolver
import json
import yaml

prev_check_json = './prev.json'
prev_check_yaml = './prev.yml'
addr_dict_old = {}
addr_dict_new = {}
addr_list = ['drive.google.com', 'mail.google.com', 'google.com']

with open(prev_check_json, 'r') as fread:
    addr_dict_old = json.load(fread)
with open(prev_check_json, 'w') as f:
    f.close

for addr in addr_list:
    answer = dns.resolver.query(addr, 'A')
    ip_a = answer[0].to_text()
    print(addr, '-', ip_a)
    addr_dict_new[f'{addr}'] = ip_a

with open(prev_check_json, 'a') as f:
    f.write(json.dumps(addr_dict_new))

with open(prev_check_yaml, 'a') as f:
    f.write(yaml.dump(addr_dict_new))

for key, value in addr_dict_new.items():
    if addr_dict_new.get(key) != addr_dict_old.get(key):
        print(f'[ERROR] {key} IP mismatch: {addr_dict_old.get(key)} {addr_dict_new.get(key)}')
