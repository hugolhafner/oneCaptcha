import os, sys
from git import Repo
from classes.logger import Logger

##### ASCII ART #####
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format
##### ASCII ART #####

class Github:
    def __init__(self):
        self.log = Logger("Git").log
        self.directory = os.path.dirname(os.path.realpath(__file__.replace("/classes", "")))
        self.repo = Repo(self.directory)

        if not self.repo.bare:
            self.log("Github Connection... [Success]", "success")
        else:
            self.log("Github Connection... [Error]", "error")

    def printCommit(self, amount=1):
        commits = list(self.repo.iter_commits('master'))[:amount]

        for commit in commits:
            print()
            self.log(f"Github Commit #{str(commit.count())}:", "note")
            self.log(f'"{commit.summary}" by {commit.author.name} ({commit.author.email})', "note")

        print()

    def reconnect(self):
        self.__init__()

def logo():
    cprint(figlet_format('oneCaptcha'), 'green', attrs=['bold'])

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

searchTerms = [
    "facebook",
    "youtube",
    "amazon",
    "ebay",
    "yahoo",
    "craigslist",
    "yahoo mail",
    "bbc weather",
    "netflix",
    "walmart",
    "news",
    "facebook login",
    "home depot",
    "cnn",
    "hotmail",
    "fox news",
    "msn",
    "usps tracking",
    "lowes",
    "enterntainment",
    "paypal",
    "barclays",
    "bank of america",
    "aol mail",
    "target",
    "espn",
    "instagram",
    "wells fargo",
    "pinterest",
    "zillow",
    "twitter",
    "speed test",
    "indeed",
    "best buy",
    "trump",
    "roblox",
    "sports",
    "linkedin",
    "aol",
    "amazon prime",
    "chase",
    "capital one",
    "pandora",
    "usp tracking",
    "costco",
    "reddit",
    "bing",
    "nba",
    "traductor",
    "kohls",
    "finance",
    "hulu",
    "american airlines",
    "usps",
    "fb",
    "pizza hut",
    "etsy",
    "airbnb",
    "twitch",
    "nfl",
    "dominos",
    "expedia",
    "spotify",
    "macys",
    "verizon",
    "github",
    "fedex tracking",
    "mapquest",
    "bed bath and beyond",
    "discord",
    "outlook",
    "pof",
    "southwest",
    "walgreens",
    "xfinity",
    "groupon",
    "thesaurus",
    "gamestop",
    "timblr",
    "autozone"
]

youtubeVideos = [

]

translationLanguages = [
    "english to german",
    "english to french",
    "english to spanish",
    "english to hungarian",
    "english to russian",
    "english to italian",
    "english to japanese",
    "english to swedish",
    "english to afrikaans"
]