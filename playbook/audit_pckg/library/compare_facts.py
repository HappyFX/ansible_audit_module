#!/usr/bin/python
from ansible.module_utils.basic import *
import codecs
import json

def compare_hosts(data, count):
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

def handler_services(data):
  result = {}
  for service_name, values in data.items():
    result.setdefault(service_name, values['status'])
  return result

def handler_packages(data):
  result = {}
  for package_name, values in data.items():
    result.setdefault(package_name, values[0]['version'])
  return result

def handler_system(data):
  result = {}
  for system_name, version in data.items():
    result.setdefault(system_name, version)
  return result

def handle_hostvars(params):
  data = params.get('data')
  dest_raw = params.get('dest_raw')
  dest_result = params.get('dest_result')
  if dest_raw:
    write_json(data, dest_raw)
  result = {}
  choice_map = {
    "services": handler_services,
    "packages": handler_packages,
    "system": handler_system,
  }
  for host, data_values in data.items():
    result.setdefault(host, {})
    for module_type, module_values in data_values.items():
      result[host].setdefault(module_type, choice_map.get(module_type)(module_values))
  result_by_modules = compare_hosts(data = result, count = len(data.keys()))
  if dest_result:
    write_json(result_by_modules, dest_result)
  return result_by_modules

def write_json(data, path):
  with codecs.open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

def main():
  fields = {
    "data": {"required": True, "type": "dict"},
    "dest_raw": {"default": False, "type": "str"},
    "dest_result": {"default": False, "type": "str"},
  }
  module = AnsibleModule(argument_spec=fields)
  response = handle_hostvars(module.params)
  module.exit_json(changed=False, meta=response)

if __name__ == '__main__':
  main()
