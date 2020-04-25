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
module: ic_is_resource_instance
short_description: Create or delete resource instance.
author: James Regis (@jregis)
version_added: "2.9"
description:
    - Create or delete resource instance on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            -  Name that has to be given to the resource instance to
               create or delete. During the removal an UUID could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the resource
            instance has to be created. If absent, the default resource
            group will be used.
        required: false
    resource_plan:
        description:
            -  Indicates the plan which will be used to deploy the resource
               instance. If absent, the DNS resource plan will be used.
        required: false
        choices: [dns, object-storage]
        default: dns
    target:
        description:
            -  Indicates where the resource instance should be deployed.
        default: bluemix-global
        required: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Create resource instance
- ic_is_resource_instance:
    name: ibmcloud-resource-instance-baby
    resource_plan: dns
    target: bluemix-global

# Create resource instance for object storage
- ic_is_resource_instance:
    instance: ibmcloud-object-resource-instance-baby
    resource_group: my-resource-group
    resource_plan: object-storage

# Delete resource instance
- ic_is_resource_instance
    name: ibmcloud-resource-instance-baby
    state: absent
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        resource_plan=dict(
            type='str',
            default='dns',
            choices=['dns', 'object-storage'],
            required=False),
        target=dict(
            type='str',
            required=False),
        state=dict(
            type='str',
            default='present',
            choices=['absent', 'present'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    resource_instance = sdk.ResourceInstance()

    name = module.params['instance']
    resource_group = module.params["resource_group"]
    target = module.params['target']
    resource_plan = module.params['resource_plan']
    state = module.params['state']

    if state == "absent":
        result = resource_instance.delete_resource_instance(name)
        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "resource instance {} doesn't exist".format(name)))

        module.exit_json(changed=True, msg=(
            "resource instance {} successfully deleted".format(name)))
    else:
        check = resource_instance.get_resource_instance(name)
        if "errors" in check:
            for key in check["errors"]:
                if key["code"] == "not_found":
                    result = resource_instance.create_resource_instance(
                            name=name,
                            resource_group=resource_group,
                            target=target,
                            resource_plan=resource_plan)
                    if "errors" in result:
                        module.fail_json(msg=result["errors"])
                    module.exit_json(changed=True, msg=result)

        module.exit_json(changed=False, msg=check)


def main():
    run_module()


if __name__ == '__main__':
    main()
