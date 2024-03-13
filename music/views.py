from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json




# Create your views here.

def top_artists():
    artist_info = []

    response_json = {
    "status": True,
    "type": "chart",
    "id": "123",
    "title": "Weekly Top Artists: Global",
    "description": "Your weekly update of the most played artists",
    "date": "2022-07-07",
    "artists": [
      {
        "name": "СЕРЕГА ПИРАТ",
        "type": "artist",
        "id": "5IS4dQ9lDW01IY1buR7bW7",
        "shareUrl": "https://open.spotify.com/artist/5IS4dQ9lDW01IY1buR7bW7",
        "visuals": {
          "avatar": [
            {
              "url": "https://i.scdn.co/image/ab6761610000e5ebf6145483a8353f6ae859feac",
              "width": 640,
              "height": 640
            }
          ]
        },
        "chartData": {
          "currentRank": 1,
          "previousRank": 1,
          "peakRank": 1,
          "peakDate": "2021-10-28",
          "entryRank": 2,
          "entryDate": "2021-10-21",
          "appearancesOnChart": 38,
          "consecutiveAppearancesOnChart": 38
        }
      },
      {
        "name": "АНТИВСЕЛЕННАЯ",
        "type": "artist",
        "id": "063CKq9soidxbrMh1QFjG4",
        "shareUrl": "https://open.spotify.com/artist/063CKq9soidxbrMh1QFjG4",
        "visuals": {
          "avatar": [
            {
              "url": "https://i.scdn.co/image/ab67616d0000b2735210e66474e1f45dcd1ba139",
              "width": 640,
              "height": 640
            }
          ]
        },
        "chartData": {
          "currentRank": 1,
          "previousRank": 1,
          "peakRank": 1,
          "peakDate": "2021-10-28",
          "entryRank": 2,
          "entryDate": "2021-10-21",
          "appearancesOnChart": 38,
          "consecutiveAppearancesOnChart": 38
        }
      }
      
    ]
  }
    if 'artists' in response_json:
        for artist in response_json['artists']:
            name = artist.get('name', 'Unknown Name')
            artist_id = artist.get('id', 'Unknown ID')
            avatar_url = artist.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
            artist_info.append((name, avatar_url, artist_id))
    else:
        artist_info = [{"name": "Unknown", "id":"0", "url":"ya.ru"}]
    return artist_info

@login_required(login_url='login')
def index(request):
    artists_info = top_artists()
    
    context = {
        'artist_info': artists_info,
    }
    return render(request, 'music/index.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password_input']

        user_login = auth.authenticate(username = username, password = password)

        if user_login is not None:
            auth.login(request, user_login)
            return redirect('/')
        else:
            messages.info(request, 'Invalid login or password')
            return redirect('login')
    else:
        return render(request, 'music/login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save()

                user_login = auth.authenticate(username = username, email = email, password = password)
                auth.login(request, user_login)
                return redirect('/')


        else:
            messages.info(request, 'Password not matched')
            return redirect('signup')
    else:
        return render(request, 'music/signup.html')
    
def profile(request, pk):
    response_json = {
        "external_urls": {
            "spotify": "https://open.spotify.com/artist/5IS4dQ9lDW01IY1buR7bW7"
        },
        "followers": {
            "href": None,
            "total": 164662
        },
        "genres": ["russian drain"],
        "href": "https://api.spotify.com/v1/artists/5IS4dQ9lDW01IY1buR7bW7?locale=en-US%2Cen%3Bq%3D0.9%2Cru%3Bq%3D0.8%2Cru-RU%3Bq%3D0.7",
        "id": "5IS4dQ9lDW01IY1buR7bW7",
        "images": [
            {
            "url": "https://i.scdn.co/image/ab6761610000e5ebf6145483a8353f6ae859feac",
            "height": 640,
            "width": 640
            },
            {
            "url": "https://i.scdn.co/image/ab67616100005174f6145483a8353f6ae859feac",
            "height": 320,
            "width": 320
            },
            {
            "url": "https://i.scdn.co/image/ab6761610000f178f6145483a8353f6ae859feac",
            "height": 160,
            "width": 160
            }
        ],
        "name": "СЕРЕГА ПИРАТ",
        "popularity": 57,
        "type": "artist",
        "uri": "spotify:artist:5IS4dQ9lDW01IY1buR7bW7"
        }

    return render(request, 'music/profile.html')

def music(request, pk):
    return render(request, 'music/music.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')
