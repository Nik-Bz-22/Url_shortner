#!/usr/bin/env python3
import aws_cdk as cdk
from url_shortener_stack import UrlShortenerStack
import os
AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
AWS_REGION = os.environ.get("AWS_REGION")

app = cdk.App()
UrlShortenerStack(app, "UrlShortenerStack", env=cdk.Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION))
app.synth()
