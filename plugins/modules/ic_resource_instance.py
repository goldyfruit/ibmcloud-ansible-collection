#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.resource import resource_instance as sdk

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_resource_instance
short_description: Manage resource instance on IBM Cloud.
author: James Regis (@jregis)
version_added: "2.9"
description:
  - The resource controller can provision or create an instance. Provisioning
    reserves a resource on a service, and the reserved resource is a service
    instance. A resource instance can vary by service.
  - Examples include a single database on a multi-tenant server, a dedicated
    cluster, or an account on a web application.
requirements:
    - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - The name of the instance. Must be 180 characters or less and cannot
        include any special characters other than (space) - . _ :.
    type: str
    required: true
  resource_group:
    description:
      - Short or long ID of resource group.
    type: str
  resource_plan:
    description:
      - The unique ID of the plan associated with the offering. This value is
        provided by and stored in the global catalog.
    type: str
  target:
    description:
      - The deployment location where the instance should be hosted.
    type: str
  tags:
    description:
      - Tags that are attached to the instance after provisioning. These tags
        can be searched and managed through the Tagging API in IBM Cloud.
    type: list
  allow_cleanup:
    description:
      - A boolean that dictates if the resource instance should be deleted
        (cleaned up) during the processing of a region instance delete call.
    type: bool
    default: false
    choices: [true, false]
  parameters:
    description:
      - Configuration options represented as key-value pairs that are passed
        through to the target resource brokers.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create resource instance
  ic_resource_instance:
    instance: ibmcloud-resource-instance-baby
    resource_plan: ibmcloud-resource-plan
    target: bluemix-global
    tags:
      - cos

- name: Delete resource instance
  ic_resource_instance:
    instance: ibmcloud-resource-instance-baby
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
            required=False),
        target=dict(
            type='str',
            required=False),
        tags=dict(
            type='list',
            required=False),
        allow_cleanup=dict(
            type='bool',
            default=False,
            choices=[True, False],
            required=False),
        parameters=dict(
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

    instance = module.params['instance']
    resource_group = module.params["resource_group"]
    target = module.params['target']
    tags = module.params['tags']
    allow_cleanup = module.params['allow_cleanup']
    parameters = module.params['parameters']
    resource_plan = module.params['resource_plan']
    state = module.params['state']

    check = resource_instance.get_resource_instance(instance)

    if state == "absent":
        if "id" in check:
            result = resource_instance.delete_resource_instance(instance)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"resource_instance": instance, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"resource_instance": instance, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        if not resource_plan:
            payload = {"errors": {"code": "resource_plan is missing"}}
            module.fail_json(msg=payload)

        result = resource_instance.create_resource_instance(
                name=instance,
                resource_group=resource_group,
                target=target,
                resource_plan=resource_plan,
                tags=tags,
                allow_cleanup=allow_cleanup,
                parameters=parameters
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
