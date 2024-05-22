import aws_cdk as cdk

from infra.stacks.remote_stack import Remote
from infra.stacks.shared_stack import WebServiceStack

app = cdk.App()

ACCOUNT = app.node.try_get_context("account_id")

ireland_env = cdk.Environment(region="eu-west-1", account=ACCOUNT)
us_env = cdk.Environment(region="us-west-1", account=ACCOUNT)

web = WebServiceStack(
    app,
    "InfraStack",
    env=ireland_env,
)

tester = Remote(
    app,
    "Remote",
    env=us_env,
)


app.synth()
