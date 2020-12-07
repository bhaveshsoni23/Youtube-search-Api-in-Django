import requests
from django.conf import settings
from isodate import parse_duration
from django.shortcuts import render,redirect
from dev_setting import setting


def index(request):
    domain_name = setting.domain_name_with_protocol
    videos = []
    if request.method == 'POST':
        platform = 'youtube'
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part':'snippet',
            'q' : request.POST['search'],
            'key':settings.YOUTUBE_DATA_API_KEY,
            'maxResults':9,
            'type':'video'
        }
        video_ids = []
        

        r = requests.get(search_url,params=search_params)
        results = r.json()
        print(results)
    

        for result in results:
            video_ids.append(result['id']['videoId'])

        if  request.POST['submit'] == 'instragram':
            return redirect(f'https://www.instagram.com/{ request.POST["search"] }')


        video_params = {
            'key':settings.YOUTUBE_DATA_API_KEY,
            'part':'snippet,contentDetails',
            'id':','.join(video_ids),
            'maxResults':9,
        }
        r = requests.get(video_url,params=video_params)
        results = r.json()['items']

        for result in results:
            video_data = {
                'title':result['snippet']['title'],
                'id':result['id'],
                'url' : f'https://www.youtube.com/embed/{ result["id"] }',
                'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds()// 60),
                'thumbnails':result['snippet']['thumbnails']['high']['url'],
                'platform':'youtube'
            }
            videos.append(video_data)
    context = {
        'videos':videos,
        'domain_name':domain_name,
    }
  
    return render(request,'search/index.html',context)            

        


def view(request):
    domain_name = setting.domain_name_with_protocol
    if(request.GET.get('vid') and request.GET.get('plt')):
        vid = request.GET['vid']
        plt = request.GET['plt']
    else:
        return redirect('search')

    if(plt == 'youtube'):
        ifram_url = f"https://www.youtube.com/embed/{vid}?autoplay=1&origin={domain_name}"
    else:
        return redirect('search')

    context = {
        'ifram_url':ifram_url,
 
    }
    return render(request,'search/view.html',context)


