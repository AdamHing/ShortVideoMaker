import uuid
import os
from multiprocessing import Process
# from numba import jit

# from moviepy.editor import *

#https://okm85hbhd9.execute-api.us-east-2.amazonaws.com/test/transactions?transactionId=6&type=PURCHASE&amount=500


#can get connection id from local event, dont have to get it from arguments from SendMessage
print("START!")
#env variables
BUCKET = os.environ['BUCKET']
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
LAMBDA_TASK_ROOT = os.environ['LAMBDA_TASK_ROOT']
AWS_REGION = os.environ['AWS_REGION']
#generate a unique name for the video object
OBJECT = str(uuid.uuid4())+ ".mp4"
ENDPOINT_URL = os.environ['ENDPOINT_URL']
URL_EXPIRE = os.environ['URL_EXPIRE']


def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

#endpoint_url="https://s2zwrp5xhd.execute-api.us-west-2.amazonaws.com/production/"
# api_client = boto3.client('apigatewaymanagementapi', endpoint_url=ENDPOINT_URL)
def lambda_handler( event, context):
    print(event)
    from VideoClips import Clipper,Stitcher
    import subprocess
    import timeit
    import boto3
    from Websocket import Websocket
    #1. Parse out query string params
    # main_link = event['queryStringParameters']['main_link']
    # peripheral_link = event['queryStringParameters']['peripheral_link']
    # # watermark_path = event['queryStringParameters']['watermark_path']
    # captions = event['queryStringParameters']['captions']
    # manual_timestamp = event['queryStringParameters']['manual_timestamp']
    
    main_link = event['main_link']
    peripheral_link = event['peripheral_link']
    captions = event['captions']
    manual_timestamp = event['manual_timestamp']
    connectionId = event["connectionId"]
    websocket = Websocket(connectionId=connectionId)
    
    tmp_folder = "/tmp"
    peripheral_video = tmp_folder+"/MCV.mp4"
    minus_timestamp = 15
    plus_timestamp = 30

    #message = event["message"]   #message from previous lambda
    #num_clips = event['queryStringParameters']['num_clips']

    #https://0hbo7j8ysj.execute-api.us-east-2.amazonaws.com/dev/clippr?main_link=https://www.youtube.com/watch?v=UQwdai4rQ-o&peripheral_link=youtube.com/watch?v=QECEC7MLM00&captions=False&manual_timestamp=500
    #https://2ehfn7i3fywacc5vwtffs4ppxa0tukbp.lambda-url.us-east-2.on.aws/?main_link=https://www.youtube.com/watch?v=UQwdai4rQ-o&peripheral_link=youtube.com/watch?v=QECEC7MLM00&captions=False&manual_timestamp=500
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, 
                                    aws_secret_access_key=SECRET_ACCESS_KEY, 
                                    region_name=AWS_REGION)
    s3_client.download_file(BUCKET, "WaterMarks/watermark.png", "/tmp/watermark.png")
    websocket.PostToConnection(message="Downloaded watermark")
    # from main import main
    # print("imported main")
    # mainprocess = main(main_link,peripheral_link,captions)
    # mainprocess.process_data()
#=================================================================================
    # Use link1, link2, num_clips, and captions as needed
    print(f"Link 1: {main_link}")
    print(f"Link 2: {peripheral_link}")
    from pytube import YouTube
    
    vid_duration = YouTube(main_link).length
    clipper = Clipper(main_link, vid_duration=vid_duration)
    
    #get timestamp 
    if manual_timestamp:
        print("using manual_timestamp")
        timestamp = int(manual_timestamp)
    elif "www.youtube.com" in main_link:
        timestamp = clipper.get_most_rewatched_timestamp()
        print("Highest point at {}s".format(timestamp))
    else:
        return "could not get timestamp"
    websocket.PostToConnection(message="got timestamp")
    print("=========0==========")

    #download main video
    def download_main_video_func():
        start_time = timeit.default_timer()
        clipper.download(minus_timestamp, timestamp,plus_timestamp)
        websocket.PostToConnection(message="Downloaded Main video")
        end_time = timeit.default_timer()
        duration = end_time-start_time
        print("duration: "+str(duration))
    
    #download peripheral video
    def download_peripheral_video():
        start_time = timeit.default_timer()
        if peripheral_link:
            YouTube(peripheral_link,use_oauth=False, allow_oauth_cache=True).streams.filter(progressive=True, file_extension='mp4').first().download(filename=peripheral_video)
        if not os.path.isfile(peripheral_video):
            YouTube("https://www.youtube.com/watch?v=Ujvy-DEA-UM",use_oauth=False, allow_oauth_cache=True).streams.filter(progressive=True, file_extension='mp4').first().download(filename=peripheral_video)
        else:
            print("MC_video already exists, using that one")
        
        end_time = timeit.default_timer()
        duration = end_time-start_time
        print("duration: "+str(duration))
        websocket.PostToConnection(message="Downloaded peripheral video")
    #download both videos at the same time
    runInParallel(download_main_video_func(),download_peripheral_video())
    
    import glob
    command = f"ffmpeg -fflags +genpts -i {glob.glob(tmp_folder+'/ClippedVideo.*')[0]} -r 24 {tmp_folder}/ClippedVideo.mp4"
    subprocess.run(command, shell=True)
    websocket.PostToConnection(message="reformated clipped video")
    # print(path_to_webm)
    # clip = VideoFileClip(path_to_webm)
    # print(os.listdir(self.tmp_folder))
    # clip.write_videofile("ClippedVideo.mp4")
    stitcher = Stitcher(tmp_folder+"/ClippedVideo.mp4",peripheral_video)
    websocket.PostToConnection(message="Stitcher")
    # stitcher.Clip(30, timestamp,30)
    print("=========1==========")
    stitcher.Crop_stitch()
    websocket.PostToConnection(message="Crop_stitch")
    print("=========2==========")
    stitcher.Audio_watermark(tmp_folder+"/StitchedVideo_no_audio.mp4",tmp_folder+"/StitchedVideo_with_audio.mp4")
    websocket.PostToConnection(message="Audio_watermark")
    print("=========3==========")
    # print(f"Number of Clips: {self.num_clips}")
    print(f"Captions: {captions}")
    print(f"Timestamp: {timestamp}")
    print("Data processed!")

    if captions == True:
        print("doing captions")
        from dynamic_subtitles import DynamicSubtitles
        DynamicSubtitles(tmp_folder+"/StitchedVideo_with_audio.mp4",tmp_folder)
    #=================================================================================
    # print("something happend at process_data")
    #upload video to s3 file. 
    s3_client.upload_file(Filename="/tmp/StitchedVideo_with_audio.mp4",Bucket=BUCKET, Key=OBJECT)
    websocket.PostToConnection(message="uploaded video to s3")
    # generate a unique ID for each video
    url = s3_client.generate_presigned_url(
                            ClientMethod='get_object',
                            Params={"Bucket": BUCKET,"Key": OBJECT},
                            ExpiresIn=URL_EXPIRE
                            )
    websocket.PostToConnection(message=f"got presigned url: {url}")
    print(url)
    #2. Construct the body of the response object
    Response = {}
    Response['url'] = url
    Response['message'] = 'Hello from Lambda land'

    websocket.PostToConnection(message=str(Response))
    websocket.PostToConnection(message="complete")


    # #Form response and post back to provided connectionId
    # response = api_client.post_to_connection(ConnectionId=connectionId, Data=json.dumps(Response).encode('utf-8'))
    # print(response)
    
# 　　   ／⌒ヽ
# 　　　/° ω°  `
# 　＿ノ ヽ　ノ ＼＿
# `/　`/ ⌒Ｙ⌒ Ｙ　ヽ
# ( 　(三ヽ人　 /　　 |
# |　ﾉ⌒＼ ￣￣ヽ　 ノ
# ヽ＿＿＿＞､＿＿_／
# 　　 ｜( 王 ﾉ〈
# 　　 /ﾐ`ー―彡ヽ
# 　　/　ヽ_／　 |.

