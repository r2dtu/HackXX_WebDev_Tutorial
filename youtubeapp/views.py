from django.shortcuts import render, HttpResponse
import requests, json

# Create your views here.
def index(request):
    return HttpResponse('404 Not Found')


def videos(request):
    API_KEY = "AIzaSyA_dZuW2zI5FXBM63OsE7DIctXwhMAib3o"
    userData = []
    if request.method == 'POST':
        username = request.POST.get('user')
        response = requests.get('https://www.googleapis.com/youtube/v3/channels?part=contentDetails,statistics&forUsername=' + username + '&key=' + API_KEY)
        req = json.loads(response.content)

        if 'items' not in req or len(req['items']) < 1:
            ERROR = 'Could not acquire data.'
            info = {}
            info['username'] = username
            info['publishedAt'] = ERROR
            info['title'] = ERROR
            info['videoId'] = ''
            info['channelId'] = ERROR
            userData.append(info)
            return render(request, 'videos.html', {'data': userData})

        playlistId = req['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        followers = req['items'][0]['statistics']['subscriberCount']
        videos = req['items'][0]['statistics']['videoCount']
        req = requests.get(
            'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + playlistId + '&key=' + API_KEY)
        jsonList = []
        jsonList.append(json.loads(req.content))
        while True:

            for data in jsonList:
                for video in data['items']:
                    info = {}
                    info['username'] = username
                    info['publishedAt'] = video['snippet']['publishedAt']
                    info['title'] = video['snippet']['title']
                    info['videoId'] = video['snippet']['resourceId']['videoId']
                    info['channelId'] = video['snippet']['channelId']
                    info['thumbnail'] = video['snippet']['thumbnails']['default']['url'] # also medium, high, standard, maxres

                    userData.append(info)

            if "nextPageToken" in data:
                nextPageToken = data['nextPageToken']
                req = requests.get(
                    'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken=' + nextPageToken +
                        '&playlistId=' + playlistId + '&key=' + API_KEY)
                jsonList = []
                jsonList.append(json.loads(req.content))
            else:
                break

    return render(request, 'videos.html', {'data': userData})

'''
{
'kind': 'youtube#playlistItemListResponse', 
'etag': '"RmznBCICv9YtgWaaa_nWDIH1_GM/xbMfmbgsu40Oj_BIiL9HQssiyn0"', 
'nextPageToken': 'CAUQAA', 
'pageInfo': {'totalResults': 171, 'resultsPerPage': 5}, 
'items': [
    {
        'kind': 'youtube#playlistItem', 
        'etag': '"RmznBCICv9YtgWaaa_nWDIH1_GM/qKI5Yg1Vl2i2-2N6r0fbQoupdS0"', 
        'id': 'VVViVzE4SlpSZ2tvX21PR201ZXI4WXpnLlRId1hfbEUtbElJ', 
        'snippet': {
            'publishedAt': '2018-01-30T09:35:59.000Z', 'channelId': 'UCbW18JZRgko_mOGm5er8Yzg', 
            'title': 'One Direction - One Way or Another (Teenage Kicks) (Live at the BRIT Awards 2013)', 
            'description': 'One Direction - One Way Or Another (Teenage Kicks) live from The BRIT Awards 2013.\n\nStream more music from One Direction here: http://smarturl.it/OneDSpotify \n\nMore from One Direction:\nDrag Me Down: https://youtu.be/Jwgf3wmiA04 \nPerfect: https://youtu.be/Ho32Oh6b4jc \nHistory: https://youtu.be/yjmp8CoZBIo \nNight Changes: https://youtu.be/syFZfO_wfMQ \nSteal My Girl: https://youtu.be/UpsKGvPjAgw \nKiss You: https://www.youtube.com/watch?v=T4cdfRohhcg \nYou & I: https://www.youtube.com/watch?v=_kqQDCxRCzM \nStory of My Life: https://www.youtube.com/watch?v=W-TE_Ys4iwM \n\nFollow One Direction:\nFacebook https://www.facebook.com/onedirectionmusic/ \nTwitter https://twitter.com/onedirection \nInstagram https://www.instagram.com/onedirection/ \n\nMore great videos here http://smarturl.it/1DVevoX \n\nSubscribe to One Direction on YouTube: http://smarturl.it/1DYT\n\nhttp://vevo.ly/YkR6Yy', 
            'thumbnails': {
                'default': {
                    'url': 'https://i.ytimg.com/vi/THwX_lE-lII/default.jpg', 
                    'width': 120, 'height': 90
                }, 
                'medium': {'url': 'https://i.ytimg.com/vi/THwX_lE-lII/mqdefault.jpg', 'width': 320, 'height': 180}, 
                'high': {'url': 'https://i.ytimg.com/vi/THwX_lE-lII/hqdefault.jpg', 'width': 480, 'height': 360}, 
                'standard': {'url': 'https://i.ytimg.com/vi/THwX_lE-lII/sddefault.jpg', 'width': 640, 'height': 480}, 
                'maxres': {'url': 'https://i.ytimg.com/vi/THwX_lE-lII/maxresdefault.jpg', 'width': 1280, 'height': 720}
            }, 
            'channelTitle': 'OneDirectionVEVO', 
            'playlistId': 'UUbW18JZRgko_mOGm5er8Yzg', 
            'position': 0, 
            'resourceId': {'kind': 'youtube#video', 'videoId': 'THwX_lE-lII'}
        }
    }
    ...
'''