#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import requests, json, datetime, urllib.parse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm
from prettytable import PrettyTable
from difflib import get_close_matches 

TIME_NOW = datetime.datetime.now().strftime("%d-%m-%Y_%I:%M:%S_%p")
MAIN_URL = "http://data.project-gxs.com/app/"
CEND = '\33[0m'
CRED = '\33[91m'
CGREEN = '\33[92m'
CYELLOW = '\33[93m'
CBLUE = '\33[94m'

parser = argparse.ArgumentParser(description=f"Download anime💖 from {CGREEN}CLI{CEND}. {CYELLOW}Impatiently!{CEND}")
group = parser.add_mutually_exclusive_group()
group.add_argument('-u', '--update', action='store_true', help=f"Update/Create the {CYELLOW}JSON{CEND} file")
args = parser.parse_args()

def load_json(file_path):
    try:
        json_content = json.load(open(file_path,"r"))
        return json_content
    except IOError as errio:
        print(f"🔥 Oops: Cannot read file: {CRED}{errio}{CEND}")
        exit()

def load_assets(file_path=None):
    directory_path = Path("assets/json")
    # Check if assets folder exist and contains files
    if directory_path.exists():
        files_in_directory = list(directory_path.iterdir())
        if len(files_in_directory) > 0:
            # The lastest file in the list of files
            latest_file = files_in_directory[0]
            print(f"💾 Latest asset found: {CYELLOW}{latest_file.name}{CEND}")
            try:
                json_content = load_json(latest_file)
                return json_content
            except:
                pass
    print(f"🍺 No assets found! {CGREEN}Running Update...{CEND}")
    return load_update(MAIN_URL)

def make_directory(dir_name):
    try:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    except IOError as errio:
        print(f"🔥 Oops: Cannot create directory!: {CRED}{errio}{CEND}")
        exit()  
    directory_path = Path(dir_name)
    return directory_path

def scraper(soup, status, json_content):
    # Initialse values
    total_episodes = total_titles = 0
    # Extract data in status catergory
    data_status = soup.find('div', id=status).div
    
    # Extract and create anime titles
    data_status_titles = data_status.find_all("h3", recursive=False)
    total_titles = len(data_status_titles)
    json_content['status'][status]['meta-data']['no_of_titles'] += total_titles
    # Extract and create a list of anime data
    data_series = data_status.find_all("div", recursive=False)

    for index_x, data_x in enumerate(tqdm(data_series, ncols=85, desc=f"🏃 Status {CYELLOW}{status}{CEND}: ")):
        # Temporary dict to store inner values
        series_details = {}
        data_seasons = data_x.find_all("h3")
        data_field = data_x.find_all("div")
        anime_title = str(data_status_titles[index_x])[4:-5]
        series_details['seasons'] = []
        for index_y, data_y in enumerate(data_field):
            series_season_episodes = {links.text.replace('[project-gxs] ', '')[0:-28] : urllib.parse.unquote('http://data.project-gxs.com/'+str(links['href'])[3:]) for links in data_y.find_all("a")}
            season_name = str(data_seasons[index_y]).replace('S', 'Season ')[4:-5]
            series_details['seasons'].append(season_name)
            series_details[season_name] = series_season_episodes
            total_episodes += len(series_season_episodes)
        json_content['status'][status]['meta-data']['total_episodes'] = total_episodes
        json_content['status'][status]['data'][anime_title] = series_details
    print(f"🍺 Found {total_titles} titles with over {total_episodes} episodes!")
        
def get_webpage(url):
    # Initialize values
    useragent = UserAgent()
    session = requests.Session()
    session.headers.update({'User-Agent': useragent.random})
    
    # load the webpage
    try:
        print(f"🍺 Request Status:",end="")
        response = session.get(MAIN_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"🔥 Oops! Something went wrong: {CRED}{err}{CEND}")
        exit()
    print(f"{CGREEN} Done!{CEND}")
    return response

def load_update(url):
    # Initialise JSON value
    json_content = {'status': {
        'complete':
            {'meta-data' :{
                'no_of_titles' : 0,
                'total_episodes': 0
            }, 'data':{} },    
        'incomplete':
            {'meta-data' :{
                'no_of_titles' : 0,
                'total_episodes': 0
            }, 'data':{} },
        }
    }

    response = get_webpage(url)
    print(f"⏳ Scraping data! please wait...")
    # Create the soup object from the response
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        scraper(soup, 'complete', json_content)
        scraper(soup, 'incomplete', json_content)
    except:
        print(f"🔥 Oops: Maybe webpage format changed or incorrect!..")
        exit()
    json_content['content_created'] = TIME_NOW

    directory_path = make_directory("assets/json")
    print(f"💾 Saving {CYELLOW}JSON{CEND} to ",end="")
    file_name = f"anime_{TIME_NOW}.json"
    file_path = directory_path / file_name

    # Create the JSON file
    try:
        with open(file_path, mode='w') as fh:  
            json.dump(json_content, fh, indent=3)
    except IOError as errio:
        print(f"🔥 Oops: Cannot write to file: {CRED}{errio}{CEND}")
        exit()
    print(f"{CGREEN}{file_path}{CEND}")
    return json_content

def display_table(anime_title_list):
    table = PrettyTable()
    table.field_names = ["SI No.", "Anime"]
    for choice_no, anime_title in enumerate(anime_title_list):
        table.add_row([choice_no+1, anime_title])
    table.add_row([choice_no+2, 'Exit'])
    print(table)

def generate_download_links(anime_title):
    print(f"🍺 Anime: {anime_title}")
    print(f"⏳ Generating! please wait...")
    directory_path = make_directory("assets/links")
    seasons_list = json_content['status']['complete']['data'][anime_title]['seasons']
    for season in seasons_list:
        download_path = make_directory(directory_path / anime_title)
        with open(download_path / f"{season}_links.txt", mode="w") as fh:
            links = json_content['status']['complete']['data'][anime_title][season].values()
            file_content = "\n".join(links)
            fh.write(file_content)
    print(f"💾 Saving links to {CGREEN}{download_path}{CEND}")

def search_anime(json_content):
    anime_to_search = input(f"🍺 Anime title to search or type exit: ")
    if anime_to_search == 'exit':
        print(f"🍺 impatient{CYELLOW}anime{CEND}downloader: {CYELLOW}Terminating{CEND}")
        exit()

    anime_actual_titles = [key for key, name in json_content['status']['complete']['data'].items()]
    anime_short_titles = [str.lower(titles.split(' --')[0]) for titles in anime_actual_titles]
    match_found = get_close_matches(anime_to_search, anime_short_titles)
    if len(match_found) > 0:
        display_table(match_found)
        try:
            choice = int(input("Enter a choice: "))
        except:
            print(f"👽 {CYELLOW}That input is out of this world!{CEND} {CRED}Invalid Input!{CEND}")
            search_anime(json_content)
        if choice <= len(match_found) and choice > 0:
            selected_title = match_found[choice-1]
            # Short title to actual title mapping
            anime_title_to_download = anime_actual_titles[anime_short_titles.index(selected_title)]
            generate_download_links(anime_title_to_download)
        elif choice == len(match_found)+1:
            pass
        else:
            print(f"👽 {CYELLOW}That input is out of this world!{CEND} {CRED}Invalid Input!{CEND}")
    else: 
        print(f"👽 {CYELLOW}That input is out of this world!{CEND} {CRED}No Match Found!{CEND}")
    search_anime(json_content)

if __name__ == '__main__':
    print(f"🙏💛 Welcome to impatient{CYELLOW}anime{CEND}downloader 💛🙏")
    try:
        if args.update:
            json_content = load_update(MAIN_URL)
        else:
            json_content = load_assets()
        search_anime(json_content)
    except KeyboardInterrupt:
        print(f"🍺 impatient{CYELLOW}anime{CEND}downloader: {CYELLOW}Terminating{CEND}")
