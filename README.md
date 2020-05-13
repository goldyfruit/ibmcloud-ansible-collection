# IBM Cloud modules for Ansible using Ansible Collections

This collection allows interactions with IBM Cloud VPC, Classic Infrastructure, etc... Modules will consume resources and make sure idempotency is respected as it should.

IBM Cloud API keys are required, to setup keys please have a look at the official [IBM Cloud documentation](https://cloud.ibm.com/docs/iam?topic=iam-manapikey).

- [IBM Cloud Access (IAM) API key](https://cloud.ibm.com/docs/iam?topic=iam-userapikey)
- [Classic Infrastructure API key](https://cloud.ibm.com/docs/iam?topic=iam-classic_keys)

## Credentials

Once API keys are generated, the information about the IBM Cloud account need to be stored into a file `~/.ibmcloud/clouds.yaml` to be read by the IBM Cloud Python SDK.

    $ mkdir ~/.ibmcloud
    $ touch ~/.ibmcloud/clouds.yaml
    $ chmod 400 ~/.ibmcloud/clouds.yaml

Multiple account credentials could be provided, `default` option receives the account name (`demo-acc`) to use.

    ---
    clouds:
    default: demo-acc
    demo-acc:
        profile: demo
        description: Credentials from my IBM Cloud demo account
        key: XxX1234567890XxX
        region: us-south
        version: 2020-04-07
        generation: 2
        cis_username: 000000_sponge.bob@sink.com
        cis_apikey: abc123def456ghi789klm0n
    prod-acc:
        profile: prod
        description: Credentials from my IBM Cloud production account
        key: XxX1234567890XxX
        region: us-south
        version: 2020-04-07
        generation: 2
        cis_username: 000000_sponge.bob@sink.com
        cis_apikey: abc123def456ghi789klm0n


## Requirements

- **ibmcloud-python-sdk 1.0.0+**
- Python 3.6+
- Ansible 2.9+

## Install

   $ ansible-galaxy collection install ibmcloud.cloud_automation

The collection will be automatically installed in `~/.ansible/collections/ansible_collections/ibmcloud/` directory.

## How to Contribute

Please read ![Contributing](CONTRIBUTING.md)
