echo "Link: $1";
echo "start_time: $2";
echo "end_time: $3";




yt-dlp -f 18 $1 --external-downloader ffmpeg --external-downloader-args "ffmpeg_i:-ss 00:00:30 -to 00:1:30" -o "%(title)s_Extract_Format18.%(ext)s"



#bash -x Download.sh https://www.youtube.com/watch?v=uzgp65UnPxA 00:00:11 00:01:00

#bash Download.sh https://www.youtube.com/watch?v=uzgp65UnPxA 30 130




#bash Download.sh https://www.youtube.com/watch?v=uzgp65UnPxA

#yt-dlp -vU -f 18 "https://www.youtube.com/watch?v=uzgp65UnPxA" --external-downloader ffmpeg --external-downloader-args "ffmpeg_i:-ss 00:00:30 -to 00:1:30" -o "%(title)s_Extract_Format18.%(ext)s"