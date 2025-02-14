from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class UrlShortenerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)



        table = dynamodb.Table(
            self, "UrlMappingTable",
            partition_key=dynamodb.Attribute(
                name="short_id",
                type=dynamodb.AttributeType.STRING
            ),
            time_to_live_attribute="expires_at"
        )

        url_shortener_lambda = _lambda.Function(
            self, "UrlShortenerFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="url_shortener.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name,
            },
        )

        table.grant_read_write_data(url_shortener_lambda)

        api = apigateway.LambdaRestApi(
            self, "UrlShortenerApi",
            handler=url_shortener_lambda,
            proxy=False
        )

        shorten_resource = api.root.add_resource("shorten")
        shorten_resource.add_method("POST")

        url_resource = api.root.add_resource("{short_id}")
        url_resource.add_method("GET")
