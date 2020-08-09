# Get diff hosts

Exmaple reports from `playbook/audit_pckg/.report`:

1. [packages](https://htmlpreview.github.io/?https://github.com/HappyFX/ansible_audit_module/blob/master/playbook/audit_pckg/.reports/packages.html)
1. [services](https://htmlpreview.github.io/?https://github.com/HappyFX/ansible_audit_module/blob/master/playbook/audit_pckg/.reports/services.html)
1. [system](https://htmlpreview.github.io/?https://github.com/HappyFX/ansible_audit_module/blob/master/playbook/audit_pckg/.reports/system.html)

## How to run

```bash
ansible-playbook -D playbook/audit_pckg/audit_pckg.yml -l my_host_group
```

## Report

Reports generating in block

```yml
  - name: Create reports directory
    file:
      state: directory
      path: "{{ playbook_dir }}/.reports"
    delegate_to: localhost
    become: False
    run_once: True

  - name: generate html
    template:
      src: html.j2
      dest: "{{ playbook_dir }}/.reports/{{ item.key }}.html"
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
      system: "{{ my_system }}"
      dest_raw: "{{ playbook_dir }}"
      dest_result: "{{ playbook_dir }}"
    register: compared_result
    delegate_to: localhost
    run_once: True
```

#### data

* required
Json from facts

```yml
  - name: set global var
    set_fact:
      my_services: "{{ my_services | default ({}) | combine( { item: hostvars[item].ansible_facts.services} ) }}"
      my_packages: "{{ my_packages | default ({}) | combine( { item: hostvars[item].ansible_facts.packages} ) }}"
      my_system: "{{ my_system | default ({}) | combine( { item: {hostvars[item].ansible_distribution: hostvars[item].ansible_distribution_version} }) }}"
    delegate_to: localhost
    run_once: True
    loop: "{{ ansible_play_hosts }}"
```

#### dest_raw

* Optional
Output raw json to path
* [example raw packages](playbook/audit_pckg/raw_packages.json)
* [example raw services](playbook/audit_pckg/raw_services.json)
* [example raw system](playbook/audit_pckg/raw_system.json)

#### dest_result

* Optional
Output result json to path

* [example result](playbook/audit_pckg/result.json)
