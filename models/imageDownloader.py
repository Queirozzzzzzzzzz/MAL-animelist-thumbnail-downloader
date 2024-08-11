import os
import json
import requests
import re

maxRetries = 5
allowed_statuses = {'completed', 'watching', 'dropped'}

def findJsonFile(dir, username):
    filename = f"{username}_animelist.json"
    filepath = os.path.join(dir, filename)

    return filepath if os.path.exists(filepath) else None

def extractImageTitlesAndUrls(filepath, min_score):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    info = []
    for item in data['data']:
        title = item['node'].get('title') 
        url = item['node']['main_picture'].get('large')
        status = item['list_status'].get('status')
        score = item['list_status'].get('score')

        if title and url and status in allowed_statuses and int(score) >= int(min_score): 
            info.append({'title': title, 'url': url}) 

    return info

def downloadImages(username, min_score):
    if not os.path.exists(f"images/{username}"):
        os.makedirs(f"images/{username}")

    filepath = findJsonFile('lists', username)
    titlesAndUrls = extractImageTitlesAndUrls(filepath, min_score)
    
    for i, info in enumerate(titlesAndUrls):
        url = info['url']
        title = info['title']

        success = True

        retries = 0
        while retries < maxRetries:
            try:
                res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
                if res.status_code != 200:
                    raise Exception("Failed to fetch the resource")
                
                filename = re.sub(r'[^\w]', '0', title)
                filepath = os.path.join("images", username, filename + '.jpg')

                if os.path.exists(filepath):
                    print(f"File {filepath} already exists. Skipping download.")
                    break
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                with open(filepath, 'wb') as file:
                    file.write(res.content)
                    
                if not filepath.lower().endswith(('.png', '.jpeg', '.jpg')):
                    raise ValueError("Downloaded file is not a .jpg image")
                
                break
                
            except Exception as e:
                print(f"Attempt {retries+1} failed to download image from {url}: {e}")
                retries += 1
                if retries >= 5:
                    print(f"Failed to download image from {url} after 5 attempts.")
                    success = False
                    
                    continue

    if success:
        return 'Done! All images downloaded successfully.'
    else:
        return 'Finished! Some images could not be downloaded.'