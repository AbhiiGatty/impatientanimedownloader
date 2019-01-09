# impatientanimedownloader 
![author](https://is.gd/author_abhiigatty_badge_green) 

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)  [![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)
## The most impatient batch anime download links generator

## Inspiration
I found myself searching through countless sites to download quality anime in batch which weren't blocked by my ISP or my college firewall and when i find one, each episode link leads to an ad which makes me wait x seconds and then give me the real link. So here's what of an impatient programer did for the next two days.

- Found a really great site which provides quality anime links after scrolling through  reddit! :heart: (But the site had the whole one file - one advert thing, so...)
- Found their API endpoints (kinda), Well they weren't really API when i started but when i got through with them they were faster, lighter, and easier to parse for all my purposed intended and yeah i overcame the advert with some common sense.
- Okay so how i made the API was to scrape the endpoint and create my very own json feed which worked like a charm.
- Then just create a menu driven program using the json to create txt files with download links.

## Packages and Dependencies
The following listed packages and instructions are given with assumption that you have a PC with Python3 already installed
### Built-in modules used 
    argparse, pathlib, json, urllib, datetime, difflib
| Package | Documentation |
| ------ | ------ |
| Requests | [http://docs.python-requests.org/en/master/](http://docs.python-requests.org/en/master/) |
| BeautifulSoup4 | [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| Tqdm | [https://tqdm.github.io/](https://tqdm.github.io/) |
| fake_useragent | [https://pypi.org/project/fake-useragent/](https://pypi.org/project/fake-useragent/) |
| PrettyTable | [https://github.com/vishvananda/prettytable](https://github.com/vishvananda/prettytable), [https://code.google.com/archive/p/prettytable/](https://code.google.com/archive/p/prettytable/) |

## Getting started :beer:

[![asciicast](https://asciinema.org/a/220561.svg)](https://asciinema.org/a/220561)

1. Install [pipenv](https://pipenv.readthedocs.io/en/latest/) in your machine
```sh
$ pip install pipenv
```
2. Click [here](https://github.com/Hitoshirenu/impatientanimedownloader/archive/master.zip) to download the repository and unzip it or run the below command
```sh
$ git clone https://github.com/Hitoshirenu/impatientanimedownloader.git
```
3. Change to the following folder `impatientanimedownloader`
```sh
$ cd impatientanimedownloader
```
4. Install all the required packages
```sh
$ pipenv install
```
5. Execute the program in two possible ways
    1. Use the `pipenv shell` and execute the program
        ```sh
        $ pipenv shell
        $ python main.py -h
        usage: main.py [-h] [-u]
        Download anime💖 from CLI. Impatiently!

        optional arguments:
          -h, --help    show this help message and exit
          -u, --update  Update/Create the JSON file
        ```
    2. Use the `pipenv run` and execute the program
        ```sh
        $ pipenv run python main.py -h
        usage: main.py [-h] [-u]
        Download anime💖 from CLI. Impatiently!

        optional arguments:
          -h, --help    show this help message and exit
          -u, --update  Update/Create the JSON file
        ```
### Example output file structure
```
assets/
├── json
│   └── anime_10-01-2019_03:49:18_AM.json
└── links
    ├── 18if -- 1 season
    │   └── Season 1_links.txt
    ├── Death Note -- 1 season
    │   └── Season 1_links.txt
    └── Shokugeki no Souma -- 3 seasons
        ├── Season 1_links.txt
        ├── Season 2_links.txt
        └── Season 3_links.txt

```


## Contributing
Please read [CONTRIBUTING.md](https://github.com/Hitoshirenu/impatientanimedownloader/blob/master/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under MIT! 
