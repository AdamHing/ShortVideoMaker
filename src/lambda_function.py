from main import main
import json
import boto3
import uuid
import os
#env variables
BUCKET = os.environ['BUCKET']
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']

def lambda_handler(event, context):
    #1. Parse out query string params
    main_link = event['queryStringParameters']['main_link']
    peripheral_link = event['queryStringParameters']['peripheral_link']
    # watermark_path = event['queryStringParameters']['watermark_path']
    captions = event['queryStringParameters']['captions']
    manual_timestamp = event['queryStringParameters']['manual_timestamp']
    #num_clips = event['queryStringParameters']['num_clips']

    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, 
                                    aws_secret_access_key=SECRET_ACCESS_KEY, 
                                    region_name="us-east-2")

    s3_client.download_file("clipperbucket", "WaterMarks/watermark.png", r"tmp\watermark.png")

    try:
        mainprocess = main(main_link,peripheral_link,captions)
        status = mainprocess.process_data()
        print(status)

        OBJECT = str(uuid.uuid4())+".mp4"
        #upload video to s3 file. 
        s3_client.upload_file(Filename="tmp/StitchedVideo_with_audio.mp4",Bucket=BUCKET, Key=OBJECT)
        # generate a unique ID for each video
        url = s3_client.generate_presigned_url(
                                ClientMethod='get_object',
                                Params={"Bucket": BUCKET,"Key": OBJECT},
                                ExpiresIn=400
                                )
    except:
        print("failed to run mainprocess")
    
    url = "fakeURL"
    #2. Construct the body of the response object
    Response = {}
    Response['url'] = url
    Response['status'] = "its working IG"
    Response['message'] = 'Hello from Lambda land'
    
    #3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(Response)

    #4. Return the response object 
    #link to s3 and status of lambda function
    return responseObject
	

#https://okm85hbhd9.execute-api.us-east-2.amazonaws.com/test/transactions?transactionId=6&type=PURCHASE&amount=500

