import aws_cdk as cdk

from infra.custom.config import DeploymentConfig
from infra.stacks.remote_stack import Remote
from infra.stacks.shared_stack import WebServiceStack

app = cdk.App()

ACCOUNT = app.node.try_get_context("account_id")

ireland_env = cdk.Environment(region="eu-west-1", account=ACCOUNT)
us_env = cdk.Environment(region="us-west-1", account=ACCOUNT)

config = DeploymentConfig(control_ip="213.32.243.173/32")


web = WebServiceStack(
    app,
    "InfraStack",
    config=config,
    env=ireland_env,
)

tester = Remote(
    app,
    "Remote",
    config=config,
    env=us_env,
)


app.synth()
