from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup as bs
import re


# OK
def top_artists():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/artists/top"

    headers = {
        "x-rapidapi-key": "422c8eefd7mshced0a35dfdb550fp1b6812jsnda27fff08d42",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)

        # Verifica se a resposta foi bem-sucedida (status 200)
        if response.status_code == 200:
            response_data = response.json()
        else:
            print(f"Erro na resposta da API: {response.status_code}"
                  "  -  Função = top_artists")
            return []

    except requests.exceptions.RequestException as e:
        # Captura erros de conexão, timeout
        print(f"Erro na requisição: {e}")
        return []

    artists_info = []
    if 'artists' in response_data:
        for artist in response_data['artists']:
            name = artist.get('name', 'No Name')
            avatar_url = artist.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
            artist_id = artist.get('id', 'No ID')

            artists_info.append({
                'name': name,
                'avatar_url': avatar_url,
                'artist_id': artist_id
            })

    return artists_info


# ok
def top_tracks():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/tracks/top"

    headers = {
        "x-rapidapi-key": "422c8eefd7mshced0a35dfdb550fp1b6812jsnda27fff08d42",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)

        # Verifica se a resposta foi bem-sucedida (status 200)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Erro na resposta da API: {response.status_code}"
                  f" -  Função: top_tracks")
            return []

    except requests.exceptions.RequestException as e:

        print(f"Erro na requisição: {e}")
        return []

    track_details = []

    # Verifica se 'tracks' está presente na resposta
    if 'tracks' in data:
        shortened_data = data['tracks'][:18]  # Limita a 18 faixas, se necessário

        # Extrai id, name, artist e cover_url
        for track in shortened_data:
            track_id = track.get('id', 'No ID')
            track_name = track.get('name', 'No Name')

            # Verifica se existe artista e capa do álbum
            artist_name = track.get('artists', [{}])[0].get('name', 'No Artist')
            cover_url = track.get('album', {}).get('cover', [{}])[0].get('url', 'No Cover')

            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url
            })

    else:
        print("Tracks not found in the response.")

    return track_details


# ok
def get_audio_etails(query):
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download"

    querystring = {"track": query}

    headers = {
        "x-rapidapi-key": "422c8eefd7mshced0a35dfdb550fp1b6812jsnda27fff08d42",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    audio_details = []

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            response_data = response.json()

            # Verifica se a chave 'youtubeVideo' e 'audio' existem
            if 'youtubeVideo' in response_data and 'audio' in response_data['youtubeVideo']:
                audio_list = response_data['youtubeVideo']['audio']
                if audio_list:
                    first_audio_url = audio_list[0].get('url', 'No URL found')
                    duration_text = audio_list[0].get('durationText', 'No duration found')

                    audio_details.append(first_audio_url)
                    audio_details.append(duration_text)
                else:
                    print("No audio data available")
            else:
                print("No 'youtubeVideo' or 'audio' key found in the response")
        else:
            print(f"Failed to fetch data, status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return ['Error retrieving audio', '']

    # Garante que a função sempre retorne ao menos um valor padrão
    if not audio_details:
        audio_details = ['No audio URL found', 'No duration available']

    return audio_details


# ainda nao
def get_track_image(track_id, track_name):
    url = 'https://open.spotify.com/track/' + track_id

    try:
        r = requests.get(url)
        r.raise_for_status()  # Levanta exceção se a requisição falhar
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3lUXoW_2yUPKkKpFEVGM04gsRowd0vCyXew&s'

    soup = bs(r.content, 'html.parser')

    image_links_html = soup.find('img', {'alt': track_name})

    if image_links_html:
        image_links = image_links_html.get('srcset', '')
    else:
        image_links = ''

    match = re.search(r'https:\/\/i\.scdn\.co\/image\/[a-zA-Z0-9]+ 640w', image_links)

    if match:
        url_640w = match.group().rstrip(' 640w')
    else:
        url_640w = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3lUXoW_2yUPKkKpFEVGM04gsRowd0vCyXew&s'  # URL de uma imagem padrão se não for encontrada

    return url_640w


# OK
def music(request, pk):
    track_id = pk

    url = "https://spotify-scraper.p.rapidapi.com/v1/track/metadata"
    querystring = {"trackId": track_id}

    headers = {
        "x-rapidapi-key": "422c8eefd7mshced0a35dfdb550fp1b6812jsnda27fff08d42",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()

            # Extraindo track_name e artist_name
            track_name = data.get("name", "No track name")
            artists_list = data.get("artists", [])
            first_artist_name = artists_list[0].get("name", "No artist found") if artists_list else "No artist found"

            # Chamadas para as funções de detalhes do áudio e imagem da música
            audio_details_query = f"{track_name} {first_artist_name}"
            audio_details = get_audio_etails(audio_details_query)
            audio_url = audio_details[0]
            duration_text = audio_details[1]

            # Recupera a imagem da faixa
            track_image = get_track_image(track_id, track_name)

            context = {
                'track_name': track_name,
                'artist_name': first_artist_name,
                'audio_url': audio_url,
                'duration_text': duration_text,
                'track_image': track_image,
            }

            return render(request, 'music.html', context)

        else:
            # Em caso de resposta com status diferente de 200
            print(f"Erro na requisição: {response.status_code}")
            return render(request, 'error.html', {'error_message': 'Não foi possível obter os dados da música.'})

    except requests.exceptions.RequestException as e:
        # Captura exceções de rede e erros HTTP
        print(f"Erro na requisição: {e}")
        return render(request, 'error.html', {'error_message': 'Erro na comunicação com a API.'})


# ok
@login_required(login_url='login')
def index(request):
    artists_info = top_artists()
    top_track_list = top_tracks()

    # divide the list into three parts
    first_six_tracks = top_track_list[:6]
    second_six_tracks = top_track_list[6:12]
    third_six_tracks = top_track_list[12:18]

    print(top_track_list)
    context = {
        'artists_info': artists_info,
        'first_six_tracks': first_six_tracks,
        'second_six_tracks': second_six_tracks,
        'third_six_tracks': third_six_tracks,
    }
    return render(request, 'index.html', context)


# ainda nao
def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')

        url = "https://spotify-scraper.p.rapidapi.com/v1/search"
        querystring = {"term": search_query, "type": "track"}

        headers = {
            "x-rapidapi-key": "422c8eefd7mshced0a35dfdb550fp1b6812jsnda27fff08d42",
            "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Verifica se a requisição teve sucesso
        except requests.exceptions.RequestException as e:
            # Adiciona uma mensagem de erro
            return render(request, 'search.html', {'error_message': f'Erro na requisição: {e}'})

        track_list = []

        if response.status_code == 200:
            data = response.json()

            # Verifica se há tracks disponiveis antes de acessar os dados
            if 'tracks' in data and 'items' in data['tracks']:
                search_results_count = data['tracks'].get("totalCount", 0)
                tracks = data['tracks']['items']

                for track in tracks:
                    track_name = track.get("name", "No Title")
                    artist_name = track['artists'][0].get("name", "Unknown Artist") if track.get(
                        'artists') else "Unknown Artist"
                    duration = track.get("durationText", "Unknown Duration")
                    trackid = track.get("id", "")

                    # Obter imagem da faixa
                    track_image = get_track_image(trackid, track_name) or "https://imgv3.fotor.com/images/blog-richtext-image/music-of-the-spheres-album-cover.jpg"

                    track_list.append({
                        'track_name': track_name,
                        'artist_name': artist_name,
                        'duration': duration,
                        'trackid': trackid,
                        'track_image': track_image,
                    })
            else:
                search_results_count = 0

        context = {
            'search_results_count': search_results_count,
            'track_list': track_list,
        }

        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')


# ainda nao
def profile(request, pk):
    artist_id = pk

    url = "https://spotify-scraper.p.rapidapi.com/v1/artist/overview"

    querystring = {"artistId": artist_id}

    headers = {
        "X-RapidAPI-Key": "02912db996msh068b089c778126bp13a9d9jsn380afeb7d573",
        "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        name = data["name"]
        monthly_listeners = data["stats"]["monthlyListeners"]
        header_url = data["visuals"]["header"][0]["url"]

        top_tracks = []

        for track in data["discography"]["topTracks"]:
            trackid = str(track["id"])
            trackname = str(track["name"])
            if get_track_image(trackid, trackname):
                trackimage = get_track_image(trackid, trackname)
            else:
                trackimage = "https://imgv3.fotor.com/images/blog-richtext-image/music-of-the-spheres-album-cover.jpg"

            track_info = {
                "id": track["id"],
                "name": track["name"],
                "durationText": track["durationText"],
                "playCount": track["playCount"],
                "track_image": trackimage
            }

            top_tracks.append(track_info)

        artist_data = {
            "name": name,
            "monthlyListeners": monthly_listeners,
            "headerUrl": header_url,
            "topTracks": top_tracks,
        }
    else:
        artist_data = {}
    return render(request, 'profile.html', artist_data)


# ok
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')


# ok
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


# ok
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


