import aws_cdk as core
import aws_cdk.assertions as assertions

from homework_3.homework_3_stack import Homework3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in homework_3/homework_3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Homework3Stack(app, "homework-3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
