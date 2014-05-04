#!/usr/bin/python

class Deployment(object):
    """
    BigPanda deployment object.

    Example:
        >> bp = bigpanda.Client(api_token='0123479abadsfgab')
        >> deployment = bp.deployment("myapp", "v1.0", "prod-app-4")
        >> deployment.start()
        ...
        >> deployment.success()

    methods:
    start():            Mark deployment as started
    success():          Mark deployment as successful
    failure(message):   Mark deployment as failed with optional error message
    """

    deployment_start_endpoint = '/data/events/deployments/start'
    deployment_end_endpoint = '/data/events/deployments/end'

    def __init__(self, client, component, version, hosts, owner=None, source=None, env=None):
        """
        Create a new deployment.

        client:     Client object. Client.deployment() passes this object for you.
        component:  Name of the application being deployed
        version:    Version of the application being deployed
        hosts:      Name or list of names of the hosts being deployed on
        owner:      Optional name of the person responsible
        source:     Optional name of the system triggering this deployment (ex: Fabric)
        env:        Optional name of the environment being deployed on (ex: stage)
        """
        if not isinstance(hosts, list):
            hosts = [ hosts ]

        self._client = client
        self.component = component
        self.version = version
        self.hosts = hosts
        self.owner = owner
        self.source = source
        self.env = env

    def start(self):
        """
        Notify BigPanda on the start of this deployment
        """
        tmp_call_data = dict( component=self.component,
                          version=self.version,
                          hosts=self.hosts,
                          owner=self.owner,
                          source=self.source,
                          env=self.env)
        call_data = dict()
        for k in tmp_call_data:
            if tmp_call_data[k] is not None:
                call_data[k] = tmp_call_data[k]

        self._client.api_call(self.deployment_start_endpoint, data=call_data)

        return self

    def success(self):
        """
        Notify BigPanda this deployment has succeeded
        """
        call_data = dict( component=self.component,
                          version=self.version,
                          hosts=self.hosts,
                          status='success')

        self._client.api_call(self.deployment_end_endpoint, call_data)

        return self

    def failure(self, message=None):
        """
        Notify BigPanda this deployment has succeeded.

        message is an optional error message.
        """
        call_data = dict( component=self.component,
                          version=self.version,
                          hosts=self.hosts,
                          status='failure')
        if message:
            call_data['errorMessage'] = message

        self._client.api_call(self.deployment_end_endpoint, call_data)

        return self
