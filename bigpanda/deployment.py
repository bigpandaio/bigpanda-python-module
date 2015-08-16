class Deployment(object):
    """
    BigPanda deployment object.

    Example:
        >> bp = bigpanda.Client(api_token='0123479abadsfgab')
        >> deployment = bp.deployment("myapp", "v1.0", "prod-app-4")
        >> deployment.send() # New deployments are of status 'start' by default
        >> try:
        ...
        >>   deployment.success() # Set .status and calls send()
        >> except Exception as e:
        >>   deployment.failure(e)

    methods:
    send():             Send deployment to server.
    start():            Mark deployment as started and send
    success():          Mark deployment as successful and send
    failure(message):   Mark deployment as failed with optional error message and send

    All methods return the deployment object on success.
    """

    _start_endpoint = '/data/events/deployments/start'
    _end_endpoint = '/data/events/deployments/end'

    def __init__(self, component, version, hosts, status='start', owner=None, env=None, message=None, client=None):
        """
        Create a new deployment.

        component:  Name of the application being deployed
        version:    Version of the application being deployed
        hosts:      Name or list of names of the hosts being deployed on
        status:     Status of the deployment. One of: start, success, failure
        owner:      Optional name of the person responsible
        env:        Optional name of the environment being deployed on (ex: stage)
        message:    Error message when status is 'fail'
        client:     Client object. Client.deployment() passes this object for you.
        """
        if not isinstance(hosts, list):
            hosts = [ hosts ]

        self.component = component
        self.version = version
        self.hosts = hosts
        self.status = status
        self.owner = owner
        self.source_system = "python"
        self.env = env
        self.message = message
        self._client = client

        self._verify_parameters()

    def send(self):
        """
        Send deployment object to server. Returns the deployment object.

        Requires the object to be initialized with `client' parameter. Use
        Client.send() otherwise.
        """
        if not self._client:
            raise Exception("No client associated. Use Client.send() instead.")
        self._client.send(self)
        
        return self

    def start(self):
        """
        Notify BigPanda on the start of this deployment.

        Equivalent to setting .status to 'start' and calling send().
        """
        self.status = 'start'
        return self.send()

    def success(self):
        """
        Notify BigPanda this deployment has succeeded

        Equivalent to setting .status to 'success' and calling send().
        """
        self.status = 'success'
        return self.send()

    def failure(self, message=None):
        """
        Notify BigPanda this deployment has succeeded.

        message is an optional error message.

        Equivalent to setting .status to 'failure' and .message, then calling send().
        """
        self.status = 'failure'
        self.message = message
        return self.send()

    def _verify_parameters(self):
        if self.status not in ('start', 'success', 'failure'):
            raise ValueError("status must be one of start, success, failure")

    def _build_payload(self):
        self._verify_parameters()

        payload = dict( component=self.component,
                        version=self.version,
                        hosts=self.hosts )

        if self.status == 'start':
            for attr in 'owner', 'source_system', 'env', 'description':
                value = getattr(self, attr, None)
                if value:
                    payload[attr] = value
        else:
            payload['status'] = self.status

        if self.status == 'failure' and self.message:
            payload['errorMessage'] = str(self.message)

        return payload

    @property
    def _endpoint(self):
        if self.status == 'start':
            return self._start_endpoint
        else:
            return self._end_endpoint
