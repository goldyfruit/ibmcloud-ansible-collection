#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import baremetal as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_baremetal_info
short_description: Retrieve VPC Baremetal on IBM Cloud.
author: James Regis (@jamesregis)
version_added: "2.9"
description:
  - Retrieve detailed information about VPC (Virtual Provate Cloud) Baremetal
    from IBM Cloud.
    Will also provide the host password if the ssh-key is provided.
notes:
  - The result contains a list of Baremetal instances.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - Restrict results to instance with ID or name matching.
    type: str
  ssh_key:
    description:
      - SSH key used to encrypt baremetal password
    type: str
'''

EXAMPLES = r'''
- name: Retrieve baremetal instances list
  ic_is_baremetal_info:

- name: Retrieve specific baremetal instance
  ic_is_baremetal_info:
    instance: ibmcloud-vsi-baby
    ssh_key: "/home/user/.ssh/id_rsa"
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=False),
        ssh_key=dict(
            type='str',
            required=False)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    baremetal_instance = sdk.Baremetal()

    instance = module.params['instance']
    ssh_key = module.params['ssh_key']

    if instance:
        result = baremetal_instance.get_server(instance)
        if "errors" in result:
            module.fail_json(msg=result)
        configuration = baremetal_instance.get_server_configuration(
            instance)
        if "errors" in configuration:
            module.fail_json(msg=configuration)
        encrypted_password = configuration['user_accounts'][0]['encrypted_password']
        if ssh_key:
            decode_password_cmd = "echo {0} | base64 -d | openssl pkeyutl -decrypt -inkey {1} -pkeyopt rsa_mgf1_md:sha256".format(
                encrypted_password,
                ssh_key)
            decoded_password = module.run_command(
                decode_password_cmd,
                use_unsafe_shell=True)
            password = decoded_password[1]
        if not ssh_key:
            password = encrypted_password
        result["password"] = password
        result["username"] = configuration["user_accounts"][0]["username"]
        result["key_name"] = configuration["keys"][0]["name"]
    else:
        result = baremetal_instance.get_servers()
        if "errors" in result:
            module.fail_json(msg=result)
        for baremetal in result['bare_metal_servers']:
            configuration = baremetal_instance.get_server_configuration(
                baremetal["id"])
            if "errors" in configuration:
                module.fail_json(msg=configuration)
            encrypted_password = configuration['user_accounts'][0]['encrypted_password']
            if ssh_key:
                decode_password_cmd = "echo {0} | base64 -d | openssl pkeyutl -decrypt -inkey {1} -pkeyopt rsa_mgf1_md:sha256".format(
                    encrypted_password,
                    ssh_key)
                decoded_password = module.run_command(
                    decode_password_cmd,
                    use_unsafe_shell=True)
                password = decoded_password[1]
            if not ssh_key:
                password = encrypted_password
            baremetal["password"] = password
            baremetal["username"] = configuration["user_accounts"][0]["username"]
            baremetal["key_name"] = configuration["keys"][0]["name"]
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
