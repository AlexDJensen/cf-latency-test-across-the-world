import logging
import os
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_ecs_patterns as ecsp,
    aws_cloudfront as cf,
    aws_cloudfront_origins as cfo,
    RemovalPolicy,
    CfnOutput as static,
)
from constructs import Construct

from infra.custom.config import DeploymentConfig


class WebServiceStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: DeploymentConfig,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "Network", max_azs=2)

        self.ecr = ecr.Repository(
            self,
            "DockerRepo",
            empty_on_delete=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.security_group = ec2.SecurityGroup(
            self, "AppSG", vpc=self.vpc, allow_all_outbound=True
        )

        self.ecs_cluster = ecs.Cluster(
            self, "Cluster", enable_fargate_capacity_providers=True, vpc=self.vpc
        )

        dirname = os.path.dirname(__file__)
        service_asset_path = os.path.join(dirname, "../..", "webservice")
        logging.info(f"service_asset_path: {service_asset_path}")

        image = ecs.ContainerImage.from_asset(
            directory=service_asset_path,
        )

        self.service = ecsp.ApplicationLoadBalancedFargateService(
            self,
            "Service",
            assign_public_ip=True,
            security_groups=[self.security_group],
            cluster=self.ecs_cluster,
            desired_count=1,
            public_load_balancer=True,
            task_image_options=ecsp.ApplicationLoadBalancedTaskImageOptions(
                image=image
            ),
        )

        # cloudfront
        self.cf = cf.Distribution(
            self,
            "CFStuff",
            default_behavior=cf.BehaviorOptions(
                origin=cfo.LoadBalancerV2Origin(
                    load_balancer=self.service.load_balancer,
                    protocol_policy=cf.OriginProtocolPolicy.HTTP_ONLY,
                )
            ),
        )

        # Outputs:
        self.lb_address = static(
            self,
            "LBAddress",
            value=self.service.load_balancer.load_balancer_dns_name,
        )

        self.cf_address = static(self, "CFAddress", value=self.cf.domain_name)
