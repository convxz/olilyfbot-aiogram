import requests, time


def cat(BOT_TOKEN, id):
    start = time.time()
    url = "https://aws.random.cat/meow"
    cat_response = requests.get(url)
    cat_link = cat_response.json()['file']

    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={id}&photo={cat_link}')
    print(time.time() - start)
    