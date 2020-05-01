#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.cis.baremetal import hardware as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_cis_baremetal_reload_os
short_description: Reload CIS baremetal server configuration on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module reloads operating system on baremetal server in CIS
    (Cloud Infrastructure).
  - Depending the configuration, the operating system could be replaced,
    firmwares upgraded, BIOS updated, LVM enabled, etc...
requirements:
  - "ibmcloud-python-sdk"
notes:
  - This module will erase everything on the drives. Backing up all data before
    reloading the operating system.
options:
  baremetal:
    description:
      - Baremetal name or ID.
    type: str
    required: true
  image:
    description:
      - Operating system image to deploy on the baremetal server. If no image
        is set the current operating system will be re-applied.
      - C(image) and C(item_prices) cannot be set together.
      - Item price ID must be used, run C(ic_cis_baremetal_image_info) module
        to retrieve this information.
    type: str
  spare_pool:
    description:
      - Server will be moved into the spare pool after an sperating system
        reload.
    type: bool
    choices: [true, false]
  provision_script_uri:
    description:
      - will be used to download and execute a customer defined script on the
        host at the end of provisioning.
    type: str
  drive_retention:
    description:
      - Primary drive will be converted to a portable storage volume during an
        operating system reload.
    type: bool
    choices: [true, false]
  erase_drives:
    description:
      - All data will be erased from drives during an sperating system reload.
    type: bool
    choices: [true, false]
  hard_drives:
    description:
      - The hard drive partitions that a server can be partitioned with.
    type: str
  image_template_id:
    description:
      - An image template ID that will be deployed to the host. If provided no
        item prices are required.
    type: str
  item_prices:
    description:
      - Item prices that the server can be configured with.
    type: dict
  enable_lvm:
    description:
      - The provision should use LVM for all logical drives.
    type: bool
    choices: [true, false]
  reset_ipmi_password:
    description:
      - The remote management cards password will be reset.
    type: bool
    choices: [true, false]
  ssh_keys:
    description:
      - SSH keys to add to the server for authentication. SSH Keys will not
        be added to servers with Microsoft Windows.
    type: list
  upgrade_bios:
    description:
      - BIOS will be updated when installing the operating system.
    type: bool
    choices: [true, false]
  upgrade_firmware:
    description:
      - Firmware on all hard drives will be updated when installing the
        operating system.
    type: bool
    choices: [true, false]
'''

EXAMPLES = r'''
- name: Retrieve baremetal images with their item price ID
  ic_cis_baremetal_image_info:

- name: Reload default operating system and configuration
  ic_cis_baremetal_reload_os:
    baremetal: ibmcloud-baremetal-baby

- name: Deploy a new operating system
  ic_cis_baremetal_reload_os:
    baremetal: ibmcloud-baremetal-baby
    image: 12429

- name: Add new items to the baremetal server
  ic_cis_baremetal_reload_os:
    baremetal: ibmcloud-baremetal-baby
    item_prices:
      - 12429
      - 45678

- name: Erase drives, enable LVM and deploy a new operating system
  ic_cis_baremetal_reload_os:
    baremetal: gtrellu-bm.ibm.cloud
    enable_lvm: true
    erase_drives: true
    image: 44992
'''


def run_module():
    module_args = dict(
        baremetal=dict(
            type='str',
            required=True),
        image=dict(
            type='str',
            required=False),
        spare_pool=dict(
            type='bool',
            choices=[True, False],
            required=False),
        provision_script_uri=dict(
            type='str',
            required=False),
        drive_retention=dict(
            type='bool',
            choices=[True, False],
            required=False),
        erase_drives=dict(
            type='bool',
            choices=[True, False],
            required=False),
        hard_drives=dict(
            type='dict',
            required=False),
        image_template_id=dict(
            type='str',
            required=False),
        item_prices=dict(
            type='list',
            required=False),
        enable_lvm=dict(
            type='bool',
            choices=[True, False],
            required=False),
        reset_ipmi_password=dict(
            type='bool',
            choices=[True, False],
            required=False),
        ssh_keys=dict(
            type='list',
            required=False),
        upgrade_bios=dict(
            type='bool',
            choices=[True, False],
            required=False),
        upgrade_firmware=dict(
            type='bool',
            choices=[True, False],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    hardware = sdk.Hardware()

    baremetal = module.params['baremetal']
    image = module.params['image']
    spare_pool = module.params['spare_pool']
    provision_script_uri = module.params['provision_script_uri']
    drive_retention = module.params['drive_retention']
    erase_drives = module.params['erase_drives']
    hard_drives = module.params['hard_drives']
    image_template_id = module.params['image_template_id']
    item_prices = module.params['item_prices']
    enable_lvm = module.params['enable_lvm']
    reset_ipmi_password = module.params['reset_ipmi_password']
    ssh_keys = module.params['ssh_keys']
    upgrade_bios = module.params['upgrade_bios']
    upgrade_firmware = module.params['upgrade_firmware']

    check = hardware.get_baremetal(baremetal)

    if check["hardwareStatus"]["status"] != "ACTIVE":
        module.fail_json(changed=False, msg="task already in progress")
    elif image and item_prices:
        module.fail_json(
          changed=False, msg="image and item_prices cannot be used together")

    if image:
        item_prices = [image]

    result = hardware.reload_os(
      baremetal=baremetal,
      spare_pool=spare_pool,
      provision_script_uri=provision_script_uri,
      drive_retention=drive_retention,
      erase_drives=erase_drives,
      hard_drives=hard_drives,
      image_template_id=image_template_id,
      item_prices=item_prices,
      enable_lvm=enable_lvm,
      reset_ipmi_password=reset_ipmi_password,
      ssh_keys=ssh_keys,
      upgrade_bios=upgrade_bios,
      upgrade_firmware=upgrade_firmware
    )

    if "errors" in result:
        module.fail_json(msg=result)

    module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
