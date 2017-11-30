import requests
try:
    import simplejson as json
except ImportError:
    import json

import config
import deployment
import alert
from requests import Session
from requests.adapters import HTTPAdapter

class Client(object):
    """
    BigPanda Client object, used to send alerts and deployments.
    """ 
    def __init__(self, api_token, app_key=None, base_url=config.base_url, timeout=10, max_retries=5, suppress_app_key=False):
        """
        Create a new Client object, used to send alerts and deployments.

        api_token:      Your organization's API token
        app_key:        Application key, required for sending alerts.
        """
        self.api_token = api_token
        self.app_key = app_key
        self.base_url = base_url
        self.time_out = timeout
        self.max_retries = max_retries
        self.suppress_app_key = suppress_app_key
        self.session = Session()

    def deployment(self, component, version, hosts, status='start', owner=None, env=None):
        """
        Return a new Deployment object associated with this client.
        
        Refer to bigpanda.Deployment for more help.
        """
        return deployment.Deployment(component, version, hosts, status, owner, env, client=self)

    def alert(self, status, subject, check=None, description=None, cluster=None, timestamp=None, primary_attr='host', secondary_attr='check', **kwargs):
        """
        Return a new Alert object associated with this client.
        
        Refer to bigpanda.Alert for more help.
        """
        return alert.Alert(status, subject, check, description, cluster, timestamp, primary_attr, secondary_attr, client=self, **kwargs)

    def send(self, data):
        """
        Send an alert or deployment object.
        
        Normally equivalent to calling .send() on the object itself, but accepts a list
        of alerts/deployment to send in a single api call.
        """

        data_type = self._get_data_type(data)

        if isinstance(data, list):
            if data_type != 'alert':
                raise TypeError('Batch mode is only supported for alerts.')

            messages = list()
            for m in data:
                messages.append(m._build_payload())
            payload = dict(alerts=messages)
            endpoint = data[0]._endpoint
        else:
            payload = data._build_payload()
            endpoint = data._endpoint

        # Deployments don't have app_key just yet
        if data_type == 'alert':
            if not self.app_key and not self.suppress_app_key:
                raise RuntimeError("app_key is not set")
            payload['app_key'] = self.app_key

        self.post_payload = payload

        self._api_call(endpoint, payload)

    def _api_call(self, endpoint, data=None):

        if self.session is None:
            self.session = Session()

        headers = {'Authorization': 'Bearer %s' % self.api_token,
                    'Content-Type': 'application/json'}

        s = requests.Session()
        s.mount(self.base_url + endpoint, HTTPAdapter(max_retries=self.max_retries))

        if data:
            self.data = data
            r = s.post(self.base_url + endpoint, data=json.dumps(data), headers=headers, timeout=self.time_out)
        else:
            r = s.get(self.base_url + endpoint, headers=headers, timeout=self.time_out)

        r.raise_for_status()

    def _get_data_type(self, data):
        if isinstance(data, list):
            return type(data[0]).__name__.lower()
        else:
            return type(data).__name__.lower()
