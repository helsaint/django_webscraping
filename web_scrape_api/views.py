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
    links_a = []
    ##We first get a list of all links with the transferdata as not everything is stored
    ##on a single page. 
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        ##Get all the links based on their class names
        links_a = soup.find_all('a', {'class': 'tm-pagination__link'})
    except:
        return JsonResponse({"Error": "error"}, safe=False)
    base_url = "https://www.transfermarkt.com"
    dict_result = {}
    for a in links_a:
        ##We then scrape the tables using the web_scrape function
        try:
            dict_result.update(web_scrape(base_url+a['href']))
        except:
            continue
    ##print(base_url+links_a[0]['href'])
    ##dict_result.update(web_scrape(base_url+links_a[0]['href']))
    
    return JsonResponse(dict_result, safe=False)
    
def web_scrape(url):
    url = url
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
        player_link = []
        for p in players_value:
            player_valuation.append(p.text)
            player_link.append('https://www.transfermarkt.com' + p.find('a', href=True)['href'])

        ##test_link = table.find_all('td', {'class':'rechts hauptlink'})
        ##for t in test_link:
        ##    print(t.find('a', href=True)['href'])

        temp_data = table.find_all('td', {'class': 'zentriert'})
        int_count = 0
        player_age = []
        for t in temp_data:
            str_age = t.text
            if(str_age != ''):
                if(int_count%2 == 1):
                    player_age.append(str_age)
                int_count = int_count + 1
        dict_result = dict(zip(player_name,zip(player_img,player_valuation,player_age, player_link)))
        return dict_result
    except:
        return {'Error':'error'}


# Create your views here.
