import time

class Alert(object):
    """
    BigPanda alert object.

    Example:
        >> bp = bigpanda.Client(api_token='0123479abadsfgab')
        >> alert = bp.alert("host1", "ping check")
        >> alert.warn()
        ...
        >> alert.crit()
        ...
        >> alert.ack()
        ...
        >> alert.ok()

    methods:
    ok:         Set alert status to OK
    warn():     Set alert status to Warning
    crit():     Set alert status to Critical
    ack():      Mark alert as acknowledged
    """

    alert_endpoint = '/data/v2/alerts'

    def __init__(self, client, app_key, subject, check=None, description=None, cluster=None, timestamp=None, primary_attr='host', secondary_attr='check', **kwargs):
        """
        Create a new alert.
        client:         Client object. Client.alert() passes this object for you
        app_key:        Application key, generated from the alerts API instructions
        subject:        Name of host/application/service etc
        check:          Specific alert about the subject
        description:    Text description of the alert
        cluster:        Name of cluster/logical group the subject is in
        timestamp:      Unix time of alert (default is now)
        primary_attr:   Primary attribute name (default is `host')
        secondary_attr: Secondary attribute name (default is `check')

        Extra custom attributes can be passed as keyword arguments.
        """

        if not subject:
            raise ValueError("Subject can't be empty")

        if not primary_attr:
            raise ValueError("Primary attribute name can't be empty")

        if check and not secondary_attr:
            raise ValueError("Secondary attribute name can't be empty")

        self._client = client
        self.app_key = app_key
        self.subject = subject
        self.check = check
        self.description = description
        self.cluster = cluster
        self.timestamp = timestamp
        self.primary_attr = primary_attr
        self.secondary_attr = secondary_attr
        self.extra_attrs = kwargs

    def _build_payload(self, status):
        payload = dict()
        payload[self.primary_attr] = str(self.subject)
        payload["primary_property"] = str(self.primary_attr)

        api_statuses = dict(ok='ok', warn='warning', crit='critical', ack='acknowledged')
        payload['status'] = api_statuses[status]

        payload['app_key'] = str(self.app_key)

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

    def ok(self):
        """
        Send the alert with status OK to BigPanda
        """
        return self._send_alert('ok')

    def warn(self):
        """
        Send the alert with status Warning to BigPanda
        """
        return self._send_alert('warn')

    def crit(self):
        """
        Send the alert with status Critical to BigPanda
        """
        return self._send_alert('crit')

    def ack(self):
        """
        Mark the alert as Acknowledged in BigPanda
        """
        return self._send_alert('ack')

    def _send_alert(self, status):
        self._verify_parameters
        payload = self._build_payload(status)
        self._client.api_call(self.alert_endpoint, payload)

        return self

    def _verify_parameters(self):
        if not self.subject:
            raise ValueError("Subject can't be empty")

        if not self.primary_attr:
            raise ValueError("Primary attribute name can't be empty")

        if self.check and not self.secondary_attr:
            raise ValueError("Secondary attribute name can't be empty")

        if not self.app_key:
            raise ValueError("App key can't be empty")

        if timestamp:
            try:
                self.timestamp = int(timestamp)
            except Exception as e:
                raise ValueError("Timestamp must be in unix time")
