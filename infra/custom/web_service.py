"""
This construct is an ECS service running behind an ALB.
"""

from aws_cdk import aws_ecs as ecs

from constructs import Construct


class WebService(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)

        

        self.cluster = ecs.Cluster(
            self,
            "cluster",
            enable_fargate_capacity_providers=True,)
        )
