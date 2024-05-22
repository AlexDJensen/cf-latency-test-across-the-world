from aws_cdk import Stack, aws_lambda as l_func, CfnOutput as static
import os
import logging
from constructs import Construct

from infra.custom.config import DeploymentConfig


class Remote(Stack):
    """
    Will use a lambda function to contact endpoints
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: DeploymentConfig,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        dirname = os.path.dirname(__file__)
        tester_asset_path = os.path.join(dirname, "../..", "tester")
        logging.info(f"Tester Asset path: {tester_asset_path}")

        func_code = l_func.DockerImageCode.from_image_asset(
            tester_asset_path,
        )

        self.func = l_func.DockerImageFunction(
            self,
            "Func",
            code=func_code,
            environment={
                "CONTROL_IP": config.control_ip,
            },
        )

        self.log_group = static(
            self, "LogGroupName", value=self.func.log_group.log_group_name
        )
