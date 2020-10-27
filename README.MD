# Get diff hosts

Exmaple reports from `playbook/audit_pckg/.report`:

1. [packages](https://htmlpreview.github.io/?https://github.com/HappyFX/ansible_audit_module/blob/master/playbook/audit_pckg/reports/html/packages.html)
1. [services](https://htmlpreview.github.io/?https://github.com/HappyFX/ansible_audit_module/blob/master/playbook/audit_pckg/reports/html/services.html)
1. [system](https://htmlpreview.github.io/?https://github.com/HappyFX/ansible_audit_module/blob/master/playbook/audit_pckg/reports/html/system.html)
1. [mount](https://htmlpreview.github.io/?https://github.com/HappyFX/ansible_audit_module/blob/master/playbook/audit_pckg/reports/html/mounts.html)

## How to run

```bash
ansible-playbook -D playbook/audit_pckg/audit_pckg.yml -l my_host_group
```

## Report

Reports generating in block

```yml
  - name: generate html
    template:
      src: html.j2
      dest: "{{ audit_pckg_folder_html_report }}/{{ item.key }}.html"
    delegate_to: localhost
    loop: "{{ compared_result['meta'] | dict2items }}"
    run_once: True
```

### Options for module

Output of module is dict

```yml
  - name: compare facts
    compare_facts:
      services: "{{ my_services }}"
      packages: "{{ my_packages }}"
      mounts: "{{ my_mounts }}"
      mounts_filter:
        - /
        - /boot
      system: "{{ my_system }}"
      dest_raw: "{{ audit_pckg_folder_json_raw }}"
      dest_result: "{{ audit_pckg_folder_json_result }}"
    register: compared_result
    delegate_to: localhost
    run_once: True
```

#### data

* required atleast one

##### services

Systemd list

```yml
  - name: set global var
    set_fact:
      my_services: "{{ my_services | default ({}) | combine( { item: hostvars[item].ansible_facts.services} ) }}"
    delegate_to: localhost
    run_once: True
    loop: "{{ ansible_play_hosts }}"
```

##### packages

Yum packages

```yml
  - name: set global var
    set_fact:
      my_packages: "{{ my_packages | default ({}) | combine( { item: hostvars[item].ansible_facts.packages} ) }}"
    delegate_to: localhost
    run_once: True
    loop: "{{ ansible_play_hosts }}"
```

##### mounts

Mount points

```yml
  - name: set global var
    set_fact:
      my_mounts: "{{ my_mounts | default ({}) | combine( { item: hostvars[item].ansible_mounts} ) }}"
    delegate_to: localhost
    run_once: True
    loop: "{{ ansible_play_hosts }}"
```

##### system

System release

```yml
  - name: set global var
    set_fact:
      my_system: "{{ my_system | default ({}) | combine( { item: {hostvars[item].ansible_distribution: hostvars[item].ansible_distribution_version} }) }}"
    delegate_to: localhost
    run_once: True
    loop: "{{ ansible_play_hosts }}"
```

#### dest_raw

* Optional
Output raw json to path
* [example raw packages](playbook/audit_pckg/reports/json_raw/raw_packages.json)
* [example raw services](playbook/audit_pckg/reports/json_raw/raw_services.json)
* [example raw mounts](playbook/audit_pckg/reports/json_raw/raw_mounts.json)
* [example raw system](playbook/audit_pckg/reports/json_raw/raw_system.json)

#### dest_result

* Optional
Output result json to path

* [example result](playbook/audit_pckg/reports/json_result/result.json)

#### mounts_filter

* Optional
Filter for mount points
