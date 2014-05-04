"""
BigPanda integration module.

Use this module to use the BigPanda API on incidents, deployments etc.

Example:

    >> import bigpanda
    >> bp = bigpanda.Client(api_token="686a68bc876dc666")
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
