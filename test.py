from pytube import YouTube

video_url = 'https://www.youtube.com/watch?v=wypVcNIH6D4' # paste here your Youube videos' url
youtube = YouTube(video_url)
video = youtube.streams.filter(res='720p', mime_type='video/mp4')[0]
video.download('.')