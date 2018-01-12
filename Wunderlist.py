from random import randint

import requests

ACCESS_TOKEN = "332c08cb64ad807d265bea88765f20ec6c843f81882aa57228b60ee0ca49"

CLIENT_ID = "8ea9ab3c56a5a558688a"
CODE = "ae846cb0400eda557ec8"
REDIRECT_URL = "https://github.com/tmallison/magicmirror"
CLIENT_SECRET = "3f8e473845a59adf33cb49c2a726cb65055fcb601707452a3848f1d1d5ff"

url = "https://www.wunderlist.com/oauth/authorize?client_id={}&redirect_uri={}&state={}".format(CLIENT_ID,
                                                                                                REDIRECT_URL,
                                                                                                randint(1000, 10000))
print(url)
# response = requests.get(url)
# print(vars(response))

def get_list():
    url = "http://a.wunderlist.com/api/v1/lists"
    head = {'X-Access-Token': ACCESS_TOKEN,
            'X-Client-ID': CLIENT_ID}

    response = requests.get(url, headers=head)

    return response.content

print(get_list())