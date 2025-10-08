from aws_cdk import (
    Stack,
    aws_elasticbeanstalk as eb,
    aws_iam as iam,
)
from constructs import Construct

class MyEbAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, s3_bucket: str, s3_key: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1️⃣ Create Elastic Beanstalk Application
        app = eb.CfnApplication(
            self,
            "MyEBApplication",
            application_name="MyEBAppDemoCDK-Lundbeck"
        )

        # 2️⃣ IAM Role for EB EC2 instances
        eb_role_arn = "arn:aws:iam::909951481895:role/aws-elasticbeanstalk-ec2-role"

        # 3️⃣ Service Role for EB
        service_role_arn = "arn:aws:iam::909951481895:role/aws-elasticbeanstalk-service-role"

        # 4️⃣ Application Version from S3
        app_version = eb.CfnApplicationVersion(
            self,
            "AppVersion",
            application_name=app.application_name,
            source_bundle=eb.CfnApplicationVersion.SourceBundleProperty(
                s3_bucket=s3_bucket,
                s3_key=s3_key
            )
        )

        # ✅ Ensure app version depends on the application
        app_version.add_depends_on(app)

        # 5️⃣ Create Elastic Beanstalk Environment
        env = eb.CfnEnvironment(
            self,
            "MyEBEnvironment",
            environment_name="MyEBEnvDemoCDK-Lundbeck",
            application_name=app.application_name,
            solution_stack_name="64bit Amazon Linux 2023 v4.7.2 running Docker",
            option_settings=[
                {
                    "namespace": "aws:autoscaling:launchconfiguration",
                    "optionName": "IamInstanceProfile",
                    "value": "aws-elasticbeanstalk-ec2-role"
                },
                {
                    "namespace": "aws:elasticbeanstalk:environment",
                    "optionName": "EnvironmentType",
                    "value": "SingleInstance"
                }
            ],
            version_label=app_version.ref  # Deploy this app version
        )

        # 6️⃣ Make environment depend on app version
        env.add_depends_on(app_version)