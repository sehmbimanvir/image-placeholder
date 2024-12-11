from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests

currencies = {
    'USD': 'US',
    'AED': 'AE',
    'GBP': 'GB'
}

def fetch(params):
    base_url = 'https://www.google.com/search'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    response = requests.get(base_url, params=params, headers=headers)
    return response.text

def search_rate(sources):
    queries = []
    for source in sources:
        queries.append({
            "q": f"{source} in INR",
        })
    
    
    # Execute in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch, queries))

    # Print results
    res = {}
    for index, item in enumerate(results):
        soup = BeautifulSoup(item, 'html.parser')
        div = soup.find('div', attrs={'data-exchange-rate': True})
        source_index = sources[index]
        res[source_index] = {
            'value': div['data-exchange-rate'],
            'flag': f"https://flagsapi.com/{currencies[source_index]}/flat/64.png"
        }

    return res

misc_controller = Blueprint('misc_controller', __name__)

@misc_controller.route('/scriptable')
def get_currency_inr():
    data = search_rate(list(currencies.keys()))
    response = requests.get('http://bcast.classicbullion.com:7767/VOTSBroadcastStreaming/Services/xml/GetLiveRateByTemplateID/classic')
    parts = response.text.split('\n')
    gold1gm = next((item for item in parts if "GOLD 1 GM" in item), None)
    finals = gold1gm.split('\t')
    return jsonify({
        'data': {
            'currencies': data,
            'gold1': {
                value: finals[4],
                image: 'https://cdn-icons-png.flaticon.com/512/9590/9590147.png'
            }
        }
    })
    
    
    