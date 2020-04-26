#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import resource_instance as sdk

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_resource_instance_info
short_description: Retrieve information about resource instance.
author: James Regis (@jregis)
version_added: "2.9"
description:
    - Retrieve information about resource instance from IBM Cloud.
notes:
    - The result will be a single or a list resource instance.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description: 
            -  Restrict results to a resource instance  with GUID or 
            name matching.
        required: false
'''

EXAMPLES = '''
# Get resource instances info
- ic_is_resource_instance_info:
  register: resource_instances

#  Get info for ibmcloud-vpc-baby 
- ic_is_resource_instance_info
    name: ibmcloud-vpc-baby

'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            default=None,
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    resource_instance = sdk.ResourceInstance()

    instance = module.params['instance']

    if instance: 
        result = resource_instance.get_resource_instance(instance)
        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "resource instance {} doesn't exist").format(name))
        else:
            module.exit_json(changed=False, msg=(result))
    else:
        result = resource_instance.get_resource_instances()
        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "resource instance {} doesn't exist").format(name))
        else:
            module.exit_json(changed=False, msg=(result))
#    module.exit_json(changed=True, msg=(
#        "resource instance {} successfully deleted").format(name))
#    existing_resource = resource_instance.get_resource_instance(name)
#    if "errors" in existing_resource:
#        for key in existing_resource["errors"]:
#            if key["code"] == "not_found":
#                # if the resource instance doesn't exist
#                result = resource_instance.create_resource_instance(
#                        name=name,
#                        resource_group=rg,
#                        target=target,
#                        resource_plan=resource_plan)
#                if "errors" in result:
#                    module.fail_json(msg=result["errors"])
#                else:
#                    module.exit_json(changed=True, msg=(
#                        "resource instance {} successfully created").format(name))
#    module.exit_json(changed=False, msg=(existing_resource))


def main():
    run_module()


if __name__ == '__main__':
    main()
