import boto3
import os
import json

class Websocket():
    def __init__(self, connectionId):
        ENDPOINT_URL = os.environ['ENDPOINT_URL']
        #ENDPOINT_URL = "https://s2zwrp5xhd.execute-api.us-west-2.amazonaws.com/production/"
        self.api_client = boto3.client('apigatewaymanagementapi', endpoint_url=ENDPOINT_URL)
        self.connectionId = connectionId

    def PostToConnection(self,message):
        self.api_client.post_to_connection(ConnectionId=self.connectionId, Data=json.dumps(message).encode('utf-8'))

