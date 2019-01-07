import requests, json, datetime, urllib.parse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm

TIME_NOW = datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
CEND    = '\33[0m'
CRED    = '\33[91m'
CGREEN  = '\33[92m'
CYELLOW = '\33[93m'
CBLUE   = '\33[94m'

# Initialise JSON value
json_object = {'status':{'complete':[], 'incomplete':[]}}

def scraper(soup, status):
    # Extract data in status catergory
    data_status = soup.find('div', id=status).div
    
    # Extract and create anime titles
    data_status_titles = data_status.find_all("h3", recursive=False)
    # Extract and create a list of anime data
    data_series = data_status.find_all("div", recursive=False)

    for index_x, data_x in enumerate(tqdm(data_series, ncols=65, desc="🍺 Status")):
        # Temporary dict to store inner values
        series_details = {}
        data_seasons = data_x.find_all("h3")
        data_field = data_x.find_all("div")
        series_details['title'] = str(data_status_titles[index_x])[4:-5]
        series_details['seasons'] = []
        for index_y, data_y in enumerate(data_field):
            series_season_episodes = {links.text.replace('[project-gxs] ','')[0:-28] : urllib.parse.unquote('http://data.project-gxs.com/'+str(links['href'])[3:]) for links in data_y.find_all("a")}
            season_name = str(data_seasons[index_y]).replace('S','Season ')[4:-5]
            series_details['seasons'].append(season_name)
            series_details[season_name] = series_season_episodes
        json_object['status'][status].append(series_details)
        

def main(main_url):
    # Initialize values
    useragent = UserAgent()
    session = requests.Session()
    session.headers.update({'User-Agent': useragent.random})

    # Get the webpage
    print(f"🍺 Request sent, URL: {CGREEN}{main_url}{CEND}")
    try:
        response = session.get(main_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print (f"🔥 Oops! Something went wrong: {CRED}{err}{CEND}")
        exit()

    print(f"🍺{CGREEN} Response Recieved! {CEND}")
    print(f"⏳{CYELLOW} Scraping! please wait....{CEND}")

    # Create the soup object of the response
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        print(f'🏃‍ Running {CYELLOW}Complete{CEND} Category...')
        scraper(soup, 'complete')
        print(f'🏃‍ Running {CYELLOW}Incomplete{CEND} Category...')
        scraper(soup, 'incomplete')
    except:
        print(f"🔥 Oops: Maybe webpage format changed or incorrect!..")
        exit()

    json_object['content_created'] = TIME_NOW
    print(f" Writitng to {CYELLOW}JSON{CEND}...")
    file_name = f"anime_{TIME_NOW}.json"
    # Create the JSON file
    try:
        with open(file_name, 'w') as fp:  
            json.dump(json_object, fp, indent=3)
    except IOError as errio:
        print(f"🔥 Oops: Cannot write to file: {CRED}{errio}{CEND}")
        exit()
    print(f"💾 File Created: {CYELLOW}{file_name}{CEND} ")
    print(f"🍺{CGREEN} Done!{CEND}")

def downloading_client(json_file):
    pass

if __name__ == '__main__':
    url = "http://data.project-gxs.com/app/"
    main(url)
