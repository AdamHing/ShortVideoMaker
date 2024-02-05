from main import process_data
import json
import boto3
import uuid

print('Loading function')
s3 = boto3.client('s3')
def lambda_handler(event, context):
    
     
    #1. Parse out query string params
    main_link = event['queryStringParameters']['main_link']
    peripheral_link = event['queryStringParameters']['peripheral_link']
    # watermark_path = event['queryStringParameters']['watermark_path']
    captions = event['queryStringParameters']['captions']
    manual_timestamp = event['queryStringParameters']['manual_timestamp']
    #num_clips = event['queryStringParameters']['num_clips']

    status = process_data(main_link,peripheral_link,captions,manual_timestamp)

    if status == "completed":
        BUCKET = "clipper_bucket"
        #path to the local output video
        path = f"tmp/outputGREEN.mp4"
        #generate file name
        OBJECT = uuid.uuid4()+ ".mp4"
        #upload video to s3 file. 
        s3.upload_file(Filename=path,Bucket=BUCKET, Key=OBJECT)
        #generate presigned url
        url = s3.generate_presigned_url(
                                        'get_object',
                                        Params={"Bucket": BUCKET,"key": OBJECT},
                                        ExpiresIn=400
                                        )
  

    #2. Construct the body of the response object
    Response = {}
    Response['status'] = status
    Response['url'] = url
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

