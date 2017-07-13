Apprenda Hosts
=========

This role enables management of Apprenda Hosts through the System Operations Center.

Requirements
------------

* Apprenda Cloud Platform v7.1 or higher
* Python requests library (`pip install requests`)
* Python apprendaapipythonclient Library (`pip install apprendaapipythonclient`)

Role Variables
--------------

`apprenda_url` - FQDN of your ACP instance (i.e, `https://apps.apprenda.com`) **Required**

`username` - Platform user to execute role actions under. **Required**

`password` - Password of the platform user. **Required**

`tenant` - Tenant Alias of the platform user. **Required**

`action` - The action to perform. This can be one of the following. Required parameters for each action are below the action. **Required**
- `get_host_state`: Gets the host state information for a specific host.
- `set_host_state`: Sets the host state for a specific host.
  - `host_name`: The name of the host to modify state for.
  - `host_state`: The node state to transition to (one of `Online`, `Reserved`, `Maintenance`).
  - `reason`: A description of why the host is being transitioned to a new state.
- `get_host_is_transitioning`: Returns the state of the host transition. `true` if the node is moving between states, `false` otherwise.

Dependencies
------------


Example Playbook
----------------

This demonstrates how to get host state and transition a host state.

```
---
- hosts: localhost
  vars:
    apprenda_url: "https://apps.apprenda.bxcr"
    username: "bxcr@apprenda.com"
    password: "password"
    tenant: "developer"
  roles:
  - role: "apprenda_hosts"
    action: "get_host_state"
    host_name: "bxcr01"
  
  - role: "apprenda_hosts"
    action: "set_host_state"
    host_name: "bxcr01"
    host_state: "Maintenance"
    reason: "Routine maintenance"
	
  - role: "apprenda_hosts"
    action: "get_host_is_transitioning"
    host_name: "bxcr01"
```

License
-------

MIT

Author Information
------------------

Please see http://www.apprenda.com for more information about the Apprenda Cloud Platform.
