import requests
import json

import config
import deployment

class Client(object):
    def __init__(self, api_token, base_url=config.base_url):
        self.api_token = api_token
        self.base_url = base_url

    def deployment(self, component, version, hosts, owner=None, env=None):
        """
        Return a new Deployment object. Refer to bigpanda.Deployment for more help.
        """
        return deployment.Deployment(self, component, version, hosts, owner, env)

    def api_call(self, endpoint, data=None):
        headers = {'Authorization': 'Bearer %s' % self.api_token,
                    'Content-Type': 'application/json'}

        if data:
            self.data = data
            r = requests.post(self.base_url + endpoint, data=json.dumps(data), headers=headers)
        else:
            r = requests.get(self.base_url + endpoint, headers=headers)

        r.raise_for_status()
