#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from email.header import Header
import requests

def authenticate(url, user, password, tenant):
    auth_url = "{0}/authentication/api/v1/sessions/developer".format(url)
    auth_data = {
        'username': user,
        'password': password,
        'tenant': tenant
    }
    resp = requests.post(auth_url, verify=False, json=auth_data)
    resp_json = resp.json()
    return resp_json['apprendaSessionToken']

def get_host_is_transitioning(authToken, url, host_name):
    apps_url = "{0}/soc/api/v1/hosts/{1}/isTransitioning".format(url, host_name)
    resp = requests.get(apps_url, verify=False, headers=authToken)
    return resp.json(), 0

def get_host_state(authToken, url, host_name):
    apps_url = "{0}/soc/api/v1/hosts/{1}/state".format(url, host_name)
    resp = requests.get(apps_url, verify=False, headers=authToken)
    return resp.json(), 0

def set_host_state(authToken, url, host_name, host_state, reason):
    apps_url = "{0}/soc/api/v1/hosts/{1}/state".format(url, host_name)
    apps_data = {
        'state': host_state,
        'reason': reason
    }
    resp = requests.put(apps_url, json=apps_data, verify=False, headers=authToken)
    if resp.status_code != 204:
        return resp.status_code, 1
    return resp.status_code, 0

def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(required=True, choices=['get_host_is_transitioning', 'get_host_state', 'set_host_state', ]),
            apprenda_url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            tenant=dict(type='str', required=True),
            host_name=dict(required=False, type='str'),
            host_state=dict(required=False, type='str'),
            reason=dict(required=False, type='str')
        )
    )

    action = module.params['action']
    apprenda_url = module.params['apprenda_url']
    username = module.params['username']
    password = module.params['password']
    tenant = module.params['tenant']
    host_name = module.params['host_name']
    host_state = module.params['host_state']
    reason = module.params['reason']

    auth_token_string = authenticate(apprenda_url, username, password, tenant)
    auth_token = { "ApprendaSessionToken": str(Header(auth_token_string, 'utf-8')) }

    if action == "get_host_is_transitioning":
        (out, rc) = get_host_is_transitioning(auth_token, apprenda_url, host_name)
    if action == "get_host_state":
        (out, rc) = get_host_state(auth_token, apprenda_url, host_name)
    if action == "set_host_state":
        (out, rc) = set_host_state(auth_token, apprenda_url, host_name, host_state, reason)

    if (rc != 0):
        module.fail_json(msg="failure", result=out)
    else:
        module.exit_json(msg="success", result=out)

if __name__ == '__main__':
    main()
