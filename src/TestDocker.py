import subprocess

subprocess.call('yt-dlp -f 18 "{0}" --external-downloader ffmpeg --external-downloader-args "ffmpeg_i:-ss {1} -to {2}" -o "%(title)s_Extract_Format18.%(ext)s"'.format("https://www.youtube.com/watch?v=uzgp65UnPxA","00:00:30","00:01:30"), shell=True)