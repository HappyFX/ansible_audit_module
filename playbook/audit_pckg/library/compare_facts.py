#!/usr/bin/python
from ansible.module_utils.basic import *
import codecs
import json

def compare_hosts(data):
  count = len(data.keys())
  result = {}
  for host, values in data.items():
    for module_type, module_values in values.items():
      result.setdefault(module_type, {})
      for key, info in module_values.items():
        result[module_type].setdefault(key, {})
        result[module_type][key].setdefault(info, [])
        result[module_type][key][info].append(host)
        if len(result[module_type][key][info]) == count:
          del result[module_type][key]
  return result

def handler_by_key(data, params):
  key = params.get('key_name')
  result = {}
  for result_key, values in data.items():
    value = values.get(key)
    if None == value: continue
    result = set_result(result, result_key, value)
  return result

def handler_by_key_in_list(data, params):
  list_index = params.get('list_index')
  key = params.get('key_name')
  result = {}
  for result_key, values in data.items():
    try:
      index = values[list_index]
    except IndexError:
      index = None
    if None == index: continue
    value = index.get(key)
    if None == value: continue
    result = set_result(result, result_key, value)
  return result

def handler_direct(data, params):
  result = {}
  for result_key, value in data.items():
    result = set_result(result, result_key, value)
  return result

def set_result(result, key, value):
  result.setdefault(key, value)
  return result

def handle_hostvars(params):
  choice_map = {
    "services": {
      'handler_type': handler_by_key,
      'key_name': 'status',
    },
    "packages": {
      'handler_type': handler_by_key_in_list,
      'list_index': 0,
      'key_name': 'version',
    },
    "system": {
      'handler_type': handler_direct,
    },
  }
  dest_raw = params.get('dest_raw')
  dest_result = params.get('dest_result')
  result = {}
  for option_name, function_params in choice_map.items():
    data_set = params.get(option_name)
    if None == data_set: continue
    write_json(data_set, dest_raw, 'raw_' + option_name)
    for host, values in data_set.items():
      result.setdefault(host, {})
      combain_result = function_params.get('handler_type')(values, function_params)
      result[host].setdefault(option_name, combain_result)
  result_by_modules = compare_hosts(result)
  write_json(result_by_modules, dest_result, 'result')
  return result_by_modules

def write_json(data_json, dest_folder, file_name):
  if dest_folder:
    path = dest_folder + '/' + file_name + '.json'
    with codecs.open(path, 'w', encoding='utf-8') as f:
      json.dump(data_json, f, ensure_ascii=False, indent=2)

def main():
  fields = {
    "services": {"required": False, "type": "dict"},
    "packages": {"required": False, "type": "dict"},
    "system": {"required": False, "type": "dict"},
    "dest_raw": {"default": False, "type": "str"},
    "dest_result": {"default": False, "type": "str"},
  }
  module = AnsibleModule(argument_spec=fields)
  response = handle_hostvars(module.params)
  module.exit_json(changed=False, meta=response)

if __name__ == '__main__':
  main()
