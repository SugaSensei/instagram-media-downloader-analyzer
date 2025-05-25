import requests
import json
import time
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.instagram.com"
GRAPHQL_URL = "https://www.instagram.com/graphql/query/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64)",
    "Accept": "application/json",
    "X-Requested-With":"XMLHttpRequest",
}

def get_initial_data(username):
    # url = f"{BASE_URL}/{username}/"
    # r = requests.get(url, headers=HEADERS)
    # if r.status_code != 200:
    #     raise Exception(f"Failed to get page: {r.status_code}")
    
    # start = r.text.find("window._sharedData = ") + len("window._sharedData = ")
    # end = r.text.find(";</script>",start)
    # json_str = r.text[start:end]
    # data = json.loads(json_str)
    # return data

    url = f"https://www.instagram.com/{username}/"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        raise Exception(f"failed to fetch page: {r.status_code}")
    
    match = re.search(r"window\.__additionalDataLoaded\('/[^']+',\s*(\{.*?\})\)", r.text)
    if not match:
        raise Exception("Could not extract initial JSON data from page.")
    
    json_str = match.group(1)
    data = json.loads(json_str)
    return data

def get_user_id_and_page_info(data):
    user = data['entry_data']['ProfilePage'][0]['graphql']['user']
    user_id = user['id']
    page_info = user['edge_owner_to_timeline_media']['page_info']
    posts = user['edge_owner_to_timeline_media']['edges']
    return user_id, page_info, posts

def get_posts(user_id, after_cursor=None):
    query_hash = "472f257a40c653c64c666ce877d59d2b"

    variables = {
        "id": user_id,
        "first":12,
    }

    if after_cursor:
        variables["after"] = after_cursor

    params = {
        "query_hash": query_hash,
        "variables": json.dumps(variables),
    }

    r = requests.get(GRAPHQL_URL, headers=HEADERS, params=params)
    if r.status_code != 200:
        raise Exception(f"failed to get posts: {r.status_code}")
    
    return r.json()

def extract_post_urls(posts):
    urls = []
    for edge in posts:
        node = edge['node']

        if node['is_video']:
            shortcode = node['shortcode']
            url = f"https://www.instagram.com/p/{shortcode}/"
            urls.append(url)
    return urls

def main(username):
    data = get_initial_data(username)
    user_id, page_info, posts = get_user_id_and_page_info(data)

    all_urls = extract_post_url(posts)

    has_next_page = page_info['has_next_page']
    end_cursor = page_info['end_cursor']

    while has_next_page:
        time.sleep(2)
        response_json = get_posts(user_id, after_cursor=end_cursor)
        edges = response_json['data']['user']['edge_owner_to_timeline_media']['edges']
        page_info = response_json['data']['user']['edge_owner_to_timeline_media']['page_info']

        new_urls = extract_post_urls(edges)
        all_urls.extend(new_urls)

        has_next_page = page_info['has_next_page']
        end_cursor = page_info['end_cursor']

    print(f"Total video posts found: {len(all_urls)}")
    return all_urls

if __name__ == "__main__":
    username = input("instagram username: ").strip()
    urls = main(username)
    for url in urls:
        print(url)