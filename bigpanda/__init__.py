"""
BigPanda integration module.

Use this module to use the BigPanda API on incidents, deployments etc.

Example:

    >> import bigpanda
    
    # Create a client object. app_key is required for alerts.
    >> bp = bigpanda.Client(api_token="686a68bc876dc666", app_key="aasdasdasd")

    # Create a new alert object associated with the client
    >> host_alert = bp.alert("warn", "host1", "cpu load")

    # Send this alert to BigPanda
    >> host_alert.send()

    # Create a new app alert
    >> app_alert = bp.alert("crit", "app1", "connections load")

    # Mark the previous alert as acknowledged
    >> host_alert.status = "ack"

    # Use the client's send() method to send both alerts in batch mode
    >> bp.send([host_alert, app_alert])

    # Send deployment info
    >> deployment = bp.deployment("myapp", "1.0.0", "prod-app-1", owner="Paul").start()
    >> try:
    ...
    deployment code here
    ...
    >>    deployment.success()
    >> except Exception as e:
          deployment.failure(str(e))

"""
from client import Client
from deployment import Deployment
from alert import Alert
