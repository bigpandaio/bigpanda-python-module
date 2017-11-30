import time

class Alert(object):
    """
    BigPanda alert object.

    Example:
        >> bp = bigpanda.Client(api_token='0123479abadsfgab')
        >> alert = bp.alert("warn", "host1", "ping check")
        >> alert.send()
        ...
        >> alert.status = 'crit'
        >> alert.send()

        # Create an alert with a custom attribute
        >> custom_alert = bp.alert("crit", "myapp", "app connections", connections=124)
        >> custom_alert.send()

        # Update alerts in batch mode
        >> custom_alert.status = 'ack'
        >> alert.status = 'ok'
        >> bp.send([alert, custom_alert])

    methods:
    send(): Send alert to server
    """

    _endpoint = '/data/v2/alerts'
    _api_statuses = dict(ok='ok', warn='warning', crit='critical', ack='acknowledged')

    def __init__(self, status, subject, check=None, description=None, cluster=None, timestamp=None, primary_attr='host', secondary_attr='check', client=None, **kwargs):
        """
        Create a new alert.
        status:         Status of alert. One of: ok, warn, crit, ack
        subject:        Primary attribute. Name of host/application/service etc.
        check:          Secondary attribute. Specific alert about the subject.
        description:    Text description of the alert
        cluster:        Name of cluster/logical group the subject is in
        timestamp:      Unix time of alert (default is now)
        primary_attr:   Primary attribute name (default is `host')
        secondary_attr: Secondary attribute name (default is `check')
        client:         Client object. Client.alert() passes this object for you

        Extra custom attributes can be passed as keyword arguments.
        """

        if not subject:
            raise ValueError("Subject can't be empty")

        if not primary_attr:
            raise ValueError("Primary attribute name can't be empty")

        if check and not secondary_attr:
            raise ValueError("Secondary attribute name can't be empty")

        self.status = status
        self.subject = subject
        self.check = check
        self.description = description
        self.cluster = cluster
        self.timestamp = timestamp
        self.primary_attr = primary_attr
        self.secondary_attr = secondary_attr
        self.extra_attrs = kwargs
        self._client = client

        self._verify_parameters()

    def _build_payload(self):
        self._verify_parameters()

        payload = dict()
        payload[self.primary_attr] = str(self.subject)
        payload["primary_property"] = str(self.primary_attr)

        try:
            payload['status'] = self._api_statuses[self.status]
        except KeyError:
            raise ValueError("status must be one of: " + ", ".join(self.api_statuses))

        if self.check:
            payload[self.secondary_attr] = str(self.check)
            payload["secondary_property"] = str(self.secondary_attr)

        if self.description:
            payload['description'] = str(self.description)

        if self.cluster:
            payload['cluster'] = str(self.cluster)

        if self.timestamp:
            payload['timestamp'] = int(self.timestamp)
        else:
            payload['timestamp'] = int(time.time())

        for attr, value in self.extra_attrs.items():
            payload[attr] = str(value)

        return payload

    def send(self):
        """
        Send alert object to server. Returns the alert object.

        Requires the object to be initialized with `client' parameter. Use
        Client.send() otherwise.
        """
        if not self._client:
            raise Exception("No client associated. Use Client.send() instead.")
        self._client.send(self)

        return self

    def _verify_parameters(self):
        if not self.subject:
            raise ValueError("Subject can't be empty")

        if not self.primary_attr:
            raise ValueError("Primary attribute name can't be empty")

        if self.check and not self.secondary_attr:
            raise ValueError("Secondary attribute name can't be empty")

        if self.timestamp:
            try:
                self.timestamp = int(self.timestamp)
            except Exception as e:
                raise ValueError("Timestamp must be in unix time")

        if self.status not in self._api_statuses:
            raise ValueError("Status must be one of: " + ", ".join(self._api_statuses))
