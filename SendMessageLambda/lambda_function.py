# not to be dockerized
#SendMessage - Needs AmazonAPIGatewayInvokeFullAccess IAM Policy
import json
import boto3
import os
import uuid 
#env variables
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
client = boto3.client('apigatewaymanagementapi', endpoint_url="https://s2zwrp5xhd.execute-api.us-west-2.amazonaws.com/production")

lambda_client = boto3.client('lambda', region_name="us-west-2",aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=SECRET_ACCESS_KEY)
def lambda_handler(event, context):
    print("test")
    print(event,type(event))
    print(event["body"],type(event["body"]))
    print(event["body"][1],type(event["body"][1]))
    #Extract connectionId from incoming event
    connectionId = event["requestContext"]["connectionId"]
    # main_link = event['queryStringParameters']['main_link']
    # peripheral_link = event['queryStringParameters']['peripheral_link']
    # captions = event['queryStringParameters']['captions']
    # manual_timestamp = event['queryStringParameters']['manual_timestamp']
    dict = json.loads(event["body"])
    main_link = dict['main_link']
    peripheral_link = dict['peripheral_link']
    captions = dict['captions']
    manual_timestamp = dict['manual_timestamp']

    params = {"connectionId":connectionId,"main_link":main_link,"peripheral_link":peripheral_link,"captions":captions,"manual_timestamp":manual_timestamp}
    print(params)
    client.post_to_connection(ConnectionId=connectionId, Data=json.dumps(str(params)).encode('utf-8'))
    
    client.post_to_connection(ConnectionId=connectionId, Data=json.dumps("Unique message so you know something changed"+ str(uuid.uuid4())).encode('utf-8'))
    
    print("test1.5")
    responseMessage = "responding..."
    lambda_response = lambda_client.invoke(
        FunctionName='Clippr', #Broadcast #ClipprFunction #Clippr
        InvocationType='Event',
        Payload=json.dumps(params).encode()
    )

    #Form response and post back to connectionId
    response = client.post_to_connection(ConnectionId=connectionId, Data=json.dumps(responseMessage).encode('utf-8'))
    return { "statusCode": 200  }

    #{"action":"SendMessage", "message":"hello test test"}

#  {
#     "action": "SendMessage",
#     "main_link": "https://www.youtube.com/watch?v=UQwdai4rQ-o",
#     "peripheral_link": "youtube.com/watch?v=QECEC7MLM00",
#     "captions": "False",
#     "manual_timestamp": 500
# }