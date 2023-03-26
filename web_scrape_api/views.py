from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json

def web_scrape_api_home(request):
    return render(request, "web_scrape_api.html", {})

@api_view(['GET'])
def web_scrape_api(request):
    url = "https://www.transfermarkt.com/premier-league/marktwerte/wettbewerb/GB1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {'class':'items'})
        ## Get images and names of players from first page
        players_img_src = table.find_all('img', {'class': 'bilderrahmen-fixed lazy lazy'})
        player_img = []
        player_name = []
        for p in players_img_src:
            player_img.append(p['data-src'])
            player_name.append(p['title'])

        ## Get valuation of players from first page
        players_value = table.find_all('td', {'class': 'rechts hauptlink'})
        player_valuation = []
        for p in players_value:
            player_valuation.append(p.text)

        temp_data = table.find_all('td', {'class': 'zentriert'})
        int_count = 0
        player_age = []
        for t in temp_data:
            str_age = t.text
            if(str_age != ''):
                if(int_count%2 == 1):
                    player_age.append(str_age)
                int_count = int_count + 1

        print(len(player_age), player_age)
        dict_result = dict(zip(player_name,zip(player_img,player_valuation,player_age)))
        return JsonResponse(dict_result, safe=False)
    except:
        return render(request, "web_scrape_api.html", {})

# Create your views here.
