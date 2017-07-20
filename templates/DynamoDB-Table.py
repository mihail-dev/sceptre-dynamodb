# Converted from DynamoDB_Table.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/
# https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2/DynamoDB_Table.template

from troposphere import Output, Parameter, Ref, Template
from troposphere.dynamodb import (KeySchema, AttributeDefinition,
                                  ProvisionedThroughput)
from troposphere.dynamodb import Table

class DynamodbTable(object):
    def __init__(self, sceptre_user_data):
        self.t = Template()

        self.t.add_description("AWS CloudFormation Sample Template: This template "
                          "demonstrates the creation of a DynamoDB table.")
        self.sceptre_user_data = sceptre_user_data
        self.add_dynamoDB_table()

        self.hashkeyname = self.t.add_parameter(Parameter(
            "HashKeyElementName",
            Description="HashType PrimaryKey Name",
            Type="String",
            AllowedPattern="[a-zA-Z0-9]*",
            MinLength="1",
            MaxLength="2048",
            ConstraintDescription="must contain only alphanumberic characters"
        ))

        self.hashkeytype = self.t.add_parameter(Parameter(
            "HashKeyElementType",
            Description="HashType PrimaryKey Type",
            Type="String",
            Default="S",
            AllowedPattern="[S|N]",
            MinLength="1",
            MaxLength="1",
            ConstraintDescription="must be either S or N"
        ))

        self.readunits = self.t.add_parameter(Parameter(
            "ReadCapacityUnits",
            Description="Provisioned read throughput",
            Type="Number",
            Default="5",
            MinValue="5",
            MaxValue="10000",
            ConstraintDescription="should be between 5 and 10000"
        ))

        self.writeunits = self.t.add_parameter(Parameter(
            "WriteCapacityUnits",
            Description="Provisioned write throughput",
            Type="Number",
            Default="10",
            MinValue="5",
            MaxValue="10000",
            ConstraintDescription="should be between 5 and 10000"
        ))

    def add_dynamoDB_table(self):
        self.dynamodbtable = self.t.add_resource(Table(
            "myDynamoDBTable",
            AttributeDefinitions=[
                AttributeDefinition(
                    AttributeName=self.sceptre_user_data["HashKeyElementName"],
                    AttributeType=self.sceptre_user_data["HashKeyElementType"]
                ),
            ],
            KeySchema=[
                KeySchema(
                    AttributeName=self.sceptre_user_data["HashKeyElementName"],
                    KeyType="HASH"
                )
            ],
            ProvisionedThroughput=ProvisionedThroughput(
                ReadCapacityUnits=self.sceptre_user_data["ReadCapacityUnits"],
                WriteCapacityUnits=self.sceptre_user_data["WriteCapacityUnits"]
            )
        ))

def sceptre_handler(sceptre_user_data):
    dynamodbtable = DynamodbTable(sceptre_user_data)
    return dynamodbtable.t.to_json()