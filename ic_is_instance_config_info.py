#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_instance_config_info
short_description: Retrieve configuration used to initialize the VSI.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve configuration used to initialize the VSI (Virtual Server
      Instance) on IBM Cloud.
notes:
    - The result contains the configuration.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Instance UUID or name.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve instance configuration
- ic_is_instance_config_info:
    instance: ibmcloud-vsi-baby

# Retrieve instance configuration and register the value
- ic_is_instance_config_info:
    instance: ibmcloud-vsi-baby
  register: config

# Display config registered value
- debug:
    var: config
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    instance = sdk.Instance()

    name = module.params['instance']

    if name:
        result = instance.get_instance_configuration(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
