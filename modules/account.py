import os, time, sys, random, requests, pickle, traceback

from selenium.webdriver import ActionChains
from termcolor import colored
from random_word import RandomWords
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from classes.logger import Logger
from classes.utils import *

class Account:
    def __init__(self, config):
        try:
            self.email = config['account'].split(':')[0]
            self.password = config['account'].split(':')[1]
        except:
            sys.exit(1)

        self.config = config
        self.randomWord = RandomWords()
        self.action = 'starting the oneCaptcha tool.'
        self.notification = None

        self.startTime = time.time()
        self.currentWatchTime = 0
        self.completedSearches = 0
        self.readStories = 0
        self.currentTranslations = 0
        self.completedEmailActions = 0

        self.maxSearches = random.randint(int(self.config['settings']['min_searches']), int(self.config['settings']['max_searches']))
        self.maxWatchTime = random.randint(int(self.config['settings']['min_watchTime']), int(self.config['settings']['max_watchTime']))
        self.maxStories = random.randint(int(self.config['settings']['min_newsStories']), int(self.config['settings']['max_newsStories']))
        self.maxTranslations = random.randint(int(self.config['settings']['min_translations']), int(self.config['settings']['max_translations']))
        self.maxEmailActions = random.randint(int(self.config['settings']['min_emailActions']), int(self.config['settings']['max_emailActions']))

        self.log = Logger(config['tid']).log

    def _safeExit(self, save=True):
        self.notification = f'Exiting oneCaptcha for account with email {self.email}'
        if save:
            self.action = 'saving the cookies for further sessions and then exiting...'
            self.saveCookies()
        else:
            self.action = 'hard stopping the current process without saving...'

        time.sleep(1)
        self.driver.quit()
        self.action = 'quit'
        sys.exit(0)

    def _getRandomSearch(self):
        roller = random.randint(1,5)
        if roller <= 2:
            return random.choice(searchTerms)
        else:
            return random.choice(self.randomWord.get_random_words())

    def _getRandomVideo(self):
        try:
            r = requests.get('https://randomyoutube.net/api/getvid?api_token=XEIfaGCJCrJjSVQybwhEo9Q9B8EX44R53MXuWzjWTkm2KFx5d2EWD6bCAp5Y')
            return "https://www.youtube.com/watch?v=" + r.json()['vid']
        except:
            return random.choice(youtubeVideos)

    def _getTranslationLanguage(self):
        try:
            return random.choice(translationLanguages)
        except:
            return 'english to german'

    def _extractURL(self):
        try:
            url = self.driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div/div/div[1]/a').get_attribute('href')
            return url
        except:
            return None

    def newTab(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
        except:
            self.driver.execute_script('window.open("https://www.google.com","_blank");')
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(random.uniform(2.0, 3.0))

    def createDriver(self):
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        if self.config['settings']['proxy'] and self.config['proxy'] != '' and self.config['proxy'] != ' ':
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = self.config['proxy']
            proxy.ssl_proxy = self.config['proxy']
            proxy.add_to_capabilities(capabilities)

        self.driver = webdriver.Firefox(capabilities=capabilities, log_path="modules/geckodriver.log",
                                        executable_path='modules/geckodriver')

    def login(self):
        for retryCount in range(0,3):
            try:
                self.action = 'starting the gmail login progress...'
                self.driver.get('https://accounts.google.com/signin/v2/identifier?continue=https://mail.google.com/mail/&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

                self.action = 'typing in the email.'
                emailField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath','//*[@id="identifierId"]')))
                ActionChains(self.driver).move_to_element(emailField).pause(random.uniform(0.01, 0.05)).perform()
                emailField.click()
                for character in self.email:
                    emailField.send_keys(character)
                    time.sleep(random.uniform(0.05, 0.15))

                time.sleep(random.uniform(1.0, 2.0))
                nextButton = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath','//*[@id="identifierNext"]/content/span')))
                ActionChains(self.driver).move_to_element(nextButton).pause(random.uniform(0.01, 0.05)).perform()
                nextButton.click()

                self.action = 'typing in the password.'
                passwordField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath','//*[@id="password"]/div[1]/div/div[1]/input')))
                ActionChains(self.driver).move_to_element(passwordField).pause(random.uniform(0.01, 0.05)).perform()
                passwordField.click()
                time.sleep(random.uniform(1.0, 2.0))

                for character in self.password:
                    passwordField.send_keys(character)
                    time.sleep(random.uniform(0.05, 0.15))

                time.sleep(random.uniform(1.0, 2.0))

                self.action = 'finishing the gmail login process...'
                loginButton = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath','//*[@id="passwordNext"]/content/span')))
                ActionChains(self.driver).move_to_element(loginButton).pause(random.uniform(0.01, 0.05)).perform()
                loginButton.click()

                if 'Tell Google how to reach you in case you forget your password, lose access, or there’s unusual activity on your account' in self.driver.page_source:
                    doneButton = self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/c-wiz/div/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div/div[2]')
                    ActionChains(self.driver).move_to_element(doneButton).pause(random.uniform(0.01, 0.05)).perform()
                    doneButton.click()

                elif "/v2/challenge/selection" in self.driver.current_url.lower() or '/signin/v2/challenge' in self.driver.current_url.lower():
                    self.action = 'waiting for a user action...'
                    notify("Verification Required!", f"Further Google Verification Required!", "")
                    self.notification = 'Please complete the action in the browser to verify the account!'
                    input('')
                    self.notification = None

                if 'mail.google.com' in self.driver.current_url or 'mail.google.co' in self.driver.current_url:
                    self.action = 'verifying successful login!'
                    self.newTab()
                    return True
                else:
                    self.notification = self.driver.current_url.lower()
                    raise TypeError
            except KeyboardInterrupt:
                self.notification = 'User Interrupted Current process... safely exiting!'
                return None
            except Exception as e:
                notify("Error Logging In!", f"Google Account login failed [{str(retryCount + 1)}/3]!", "")
                self.notification = f'Error Logging into the google account, retry number [{str(retryCount + 1)}/3]'
                self.action = traceback.format_exc()
                time.sleep(30)

        notify("Failed Login!", "Google Account login failed 3 times, exiting account process!", "")
        self.notification = f'Failed to log into the google account with 3 retries, exiting account process!'
        return False

    def startSearch(self):
        searchesNow = random.randint(1, self.maxSearches)

        for searchNumber in range(0, searchesNow):
            try:
                searchTerm = self._getRandomSearch()
                if self.completedSearches >= self.maxSearches:
                    return

                self.action = f'searching for the term "{str(searchTerm)}" [{str(searchNumber + 1)}/{str(searchesNow)}]'
                if self.driver.current_url.lower() == 'https://www.google.co.uk/' or self.driver.current_url.lower() == 'https://www.google.co.uk':
                    searchField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', '//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input')))
                    ActionChains(self.driver).move_to_element(searchField).pause(random.uniform(0.01, 0.05)).perform()
                    searchField.click()

                    for character in searchTerm:
                        searchField.send_keys(character)
                        time.sleep(random.uniform(0.05, 0.15))

                    searchField.send_keys(Keys.ENTER)
                else:
                    searchURL = 'https://www.google.com/search?client=firefox-b-ab&q=' + searchTerm
                    self.driver.get(searchURL)

                time.sleep(random.uniform(1.0, 2.0))

                roller = random.randint(1, 3)
                if roller == 1:
                    link = self._extractURL()
                    if link != None:
                        self.driver.get(link)
                    else:
                        try:
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(random.uniform(0.2, 0.4))
                            roller = random.randint(1, 2)
                            try:
                                if roller == 1:
                                    nextPageButton = WebDriverWait(self.driver, 10).until(
                                        expected_conditions.presence_of_element_located(('xpath', '//*[@id="pnnext"]')))
                                    ActionChains(self.driver).move_to_element(nextPageButton).pause(
                                        random.uniform(0.01, 0.05)).perform()
                                    nextPageButton.click()
                                    time.sleep(random.uniform(1.0, 2.0))
                            except:
                                pass
                        except:
                            pass

                self.completedSearches += 1
                time.sleep(random.uniform(3.0, 14.0))
            except:
                continue

    def startYoutube(self, duration=180):
        beginningWatchTime = time.time()
        endWatchTime = duration + beginningWatchTime

        try:
            selectedVideo = self._getRandomVideo()
            self.driver.get(selectedVideo)
            self.action = f'watching the video {selectedVideo} for {str(endWatchTime - beginningWatchTime).split(".")[0]}s'

            while self.currentWatchTime <= self.maxWatchTime and endWatchTime >= time.time():
                time.sleep(0.99)
                self.currentWatchTime += 1

            try:
                logoButton = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', '//*[@id="logo"]')))
                ActionChains(self.driver).move_to_element(logoButton).pause(random.uniform(0.01, 0.05)).perform()
                logoButton.click()
            except:
                self.driver.get('https://youtube.com')

        except:
            pass

    def startTranslating(self):
        translationsNow = random.randint(1, self.maxTranslations)

        for translation in range(0, translationsNow):
            try:
                translationTerm = self._getRandomSearch()
                if self.currentTranslations >= self.maxTranslations:
                    return

                try:
                    self.driver.get("https://www.google.co.uk/")
                    if self.driver.current_url.lower() == 'https://www.google.co.uk/' or self.driver.current_url.lower() == 'https://www.google.co.uk':
                        translationLanguage = self._getTranslationLanguage()
                        self.action = f'translating the term "{str(translationTerm)}" with language "{str(translationLanguage)}"'
                        searchField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', '//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input')))
                        ActionChains(self.driver).move_to_element(searchField).pause(random.uniform(0.01, 0.05)).perform()
                        searchField.click()

                        for character in "google translate " + translationLanguage:
                            searchField.send_keys(character)
                            time.sleep(random.uniform(0.05, 0.15))

                        searchField.send_keys(Keys.ENTER)

                        languageField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', '//*[@id="tw-source-text-ta"]')))
                        ActionChains(self.driver).move_to_element(languageField).pause(random.uniform(0.1, 0.3)).perform()
                        languageField.click()
                        for character in translationTerm:
                            languageField.send_keys(character)
                            time.sleep(random.uniform(0.05, 0.15))
                    else:
                        raise Exception
                except Exception as e:
                    self.action = e
                    time.sleep(10)
                    languageURLs = ["https://translate.google.com/#view=home&op=translate&sl=auto&tl=es&text={}",
                                    "https://translate.google.com/#view=home&op=translate&sl=auto&tl=ar&text={}",
                                    "https://translate.google.com/#view=home&op=translate&sl=auto&tl=it&text={}"]

                    languageURL = random.choice(languageURLs)
                    self.action = f'translating the term "{str(translationTerm)}" with language "{str(languageURL)}"'
                    self.driver.get(languageURL.format(translationTerm))

                    languageField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', '//*[@id="source"]')))
                    ActionChains(self.driver).move_to_element(languageField).pause(random.uniform(0.01, 0.05)).perform()
                    languageField.click()
                    for character in translationTerm:
                        languageField.send_keys(character)
                        time.sleep(random.uniform(0.05, 0.15))

                self.currentTranslations += 1
                time.sleep(random.uniform(8.0, 35.0))
            except:
                continue

    def startNews(self):
        self.action = "starting google news function"
        storiesNow = random.randint(1, self.maxStories)

        for story in range(0, storiesNow):
            try:
                if self.readStories >= self.maxStories:
                    return

                try:
                    self.action = f'looking at the new google news headlines'
                    if 'news.google.com/topics/' not in self.driver.current_url.lower():
                        self.driver.get("https://news.google.com/?tab=wn&hl=en-GB&gl=GB&ceid=GB:en")
                        moreHeadlinesButton = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', '//*[@id="yDmH0d"]/c-wiz/div/div[1]/div/main/c-wiz/div[1]/div[1]/div[2]/a')))
                        ActionChains(self.driver).move_to_element(moreHeadlinesButton).pause(random.uniform(0.01, 0.05)).perform()
                        moreHeadlinesButton.click()

                    newsCategories = {
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/c-wiz/div/div[2]/div[1]/div[2]/div[1]/content/div': {'article': '//*[@id="tabCAQqKggAKiYICiIgQ0JBU0Vnb0lMMjB2TURWcWFHY1NBbVZ1R2dKSFFpZ0FQAQ"]/div/div/main/c-wiz/div[1]/div[{}]/div/article/a'},
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/c-wiz/div/div[2]/div[1]/div[2]/div[2]/content/div': {'article': '//*[@id="tabCAQiNkNCQVNJZ29JTDIwdk1EVnFhR2NTQW1WdUdnSkhRaUlPQ0FRYUNnb0lMMjB2TURkemMyTW9BQSoqCAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pIUWlnQVABUAE"]/div/div/main/c-wiz/div[1]/div[{}]/div/article/a'},
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/c-wiz/div/div[2]/div[1]/div[2]/div[3]/content/div': {'article': '//*[@id="tabCAQiNkNCQVNJZ29JTDIwdk1EVnFhR2NTQW1WdUdnSkhRaUlPQ0FRYUNnb0lMMjB2TURsdWJWOG9BQSoqCAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pIUWlnQVABUAE"]/div/div/main/c-wiz/div[1]/div[{}]/div/article/a'},
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/c-wiz/div/div[2]/div[1]/div[2]/div[4]/content/div': {'article': '//*[@id="tabCAQiNkNCQVNJZ29JTDIwdk1EVnFhR2NTQW1WdUdnSkhRaUlPQ0FRYUNnb0lMMjB2TURsek1XWW9BQSoqCAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pIUWlnQVABUAE"]/div/div/main/c-wiz/div[1]/div[{}]/div/article/a'},
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/c-wiz/div/div[2]/div[1]/div[2]/div[5]/content/div': {'article': '//*[@id="tabCAQiNkNCQVNJZ29JTDIwdk1EVnFhR2NTQW1WdUdnSkhRaUlPQ0FRYUNnb0lMMjB2TURkak1YWW9BQSoqCAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pIUWlnQVABUAE"]/div/div/main/c-wiz/div[1]/div[{}]/div/article/a'}
                    }

                    category = random.choice(list(newsCategories))
                    categoryField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', category)))
                    ActionChains(self.driver).move_to_element(categoryField).pause(random.uniform(0.01, 0.05)).perform()
                    categoryField.click()

                    self.action = 'found a category and looking for a news headline to read!'
                    randomStory = random.randint(1, 3)
                    storyField = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', newsCategories[category]['article'].format(str(randomStory)))))
                    ActionChains(self.driver).move_to_element(storyField).pause(random.uniform(0.01, 0.05)).perform()
                    storyField.click()
                    self.action = 'reading the news story!'
                except Exception as e:
                    self.action = e
                    time.sleep(10)
                    continue

                self.readStories += 1
                time.sleep(random.uniform(12.0, 35.0))

                while len(self.driver.window_handles) > 2:
                    self.driver.switch_to.window(self.driver.window_handles[2])
                    self.driver.close()
                    time.sleep(random.uniform(1.0, 2.0))

                try:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                except:
                    pass
            except:
                continue

    def startEmail(self):
        self.action = "completing email actions!"
        actionsNow = random.randint(1, self.maxEmailActions)

        for action in range(0, actionsNow):
            try:
                if self.completedEmailActions >= self.maxEmailActions:
                    self.newTab()

                try:
                    time.sleep(random.uniform(0.5, 2.0))
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    if "https://mail.google.com/mail/u/0/#inbox" in self.driver.current_url or "http://mail.google.com/mail/u/0/#inbox" in self.driver.current_url:
                        pass
                    else:
                        self.driver.get("https://mail.google.com/mail/u/0/?tab=wm")

                    #star, delete, archive, refresh, unread, read
                    emails = self.driver.find_elements(by='class name', value='zA')
                    email = random.choice(emails)

                    roller = random.randint(1, 5)
                    roller = 4
                    if roller == 1:
                        # Star
                        self.action = "starring a random email!"
                        starButtons = self.driver.find_elements(by='class name', value='aXw')
                        star = random.choice(starButtons)
                        self.driver.execute_script("arguments[0].scrollIntoView();", star)
                        ActionChains(self.driver).move_to_element(star).pause(random.uniform(0.1, 0.3)).perform()
                        star.click()
                    elif roller == 2:
                        # Delete
                        self.action = "deleting a random email!"
                        self.driver.execute_script("arguments[0].scrollIntoView();", email)
                        ActionChains(self.driver).move_to_element(email).pause(random.uniform(0.1, 0.3)).perform()
                        delete = email.find_element(by='class name', value='bru')
                        ActionChains(self.driver).move_to_element(delete).pause(random.uniform(0.1, 0.3)).perform()
                        delete.click()
                    elif roller == 3:
                        # Archive
                        self.action = "archiving a random email!"
                        self.driver.execute_script("arguments[0].scrollIntoView();", email)
                        ActionChains(self.driver).move_to_element(email).pause(random.uniform(0.1, 0.3)).perform()
                        archive = email.find_element(by='class name', value='brq')
                        ActionChains(self.driver).move_to_element(archive).pause(random.uniform(0.1, 0.3)).perform()
                        archive.click()
                    elif roller == 4:
                        # Mark as Unread
                        self.action = "marking a random email as unread!"
                        self.driver.execute_script("arguments[0].scrollIntoView();", email)
                        ActionChains(self.driver).move_to_element(email).pause(random.uniform(0.1, 0.3)).perform()
                        unread = email.find_element(by='class name', value='brs')
                        ActionChains(self.driver).move_to_element(unread).pause(random.uniform(0.1, 0.3)).perform()
                        unread.click()
                    elif roller == 5:
                        # Refresh
                        self.action = "refreshing emails!"
                        refreshButton = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(('xpath', '//*[@id=":5"]/div/div[1]/div[1]/div/div/div[5]/div')))
                        self.driver.execute_script("arguments[0].scrollIntoView();", refreshButton)
                        ActionChains(self.driver).move_to_element(refreshButton).pause(random.uniform(0.1, 0.3)).perform()
                        refreshButton.click()

                    time.sleep(random.uniform(2.0, 8.0))
                except Exception as e:
                    self.action = traceback.format_exc()
                    time.sleep(100)

                self.completedEmailActions += 1
            except:
                continue

        self.newTab()

    def checkScore(self):
        pass

    def saveCookies(self):
        for _ in range(0,3):
            try:
                #if "www.google.com" not in self.driver.current_url and "://google.com" not in self.driver.current_url:
                self.driver.get("https://myaccount.google.com")
                pickle.dump(self.driver.get_cookies(), open(f"sessions/google_{str(self.email).lower()}.pkl", "wb+"))
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(1, 3))
                except:
                    pass

                break
            except Exception as e:
                pass

        for _ in range(0,3):
            try:
                try:
                    if self.driver.current_url.lower() == ("https://google.com") or self.driver.current_url.lower() == ("http://google.com") or self.driver.current_url.lower() == ("https://google.com/") or self.driver.current_url.lower() == ("http://google.com/"):
                        self.driver.execute_script("window.scrollTo(0, 0;")
                        googleAppButton = self.driver.find_element_by_xpath('//*[@id="gbwa"]/div[1]/a')
                        ActionChains(self.driver).move_to_element(googleAppButton).pause(random.uniform(0.01, 0.05)).perform()
                        googleAppButton.click()

                        youtubeButton = self.driver.find_element_by_xpath('//*[@id="gb36"]')
                        ActionChains(self.driver).move_to_element(youtubeButton).pause(random.uniform(0.01, 0.05)).perform()
                        youtubeButton.click()
                except:
                    pass

                if "www.youtube.com" not in self.driver.current_url and "://youtube.com" not in self.driver.current_url:
                    self.driver.get('https://www.youtube.com')

                pickle.dump(self.driver.get_cookies(), open(f"sessions/youtube_{str(self.email).lower()}.pkl", "wb+"))
                time.sleep(random.uniform(1, 3))

                break
            except Exception as e:
                pass

    def readCookies(self):
        self.action = "checking if previous session is present..."

        sessionFiles = os.listdir('sessions')
        if f'google_{str(self.email).lower()}.pkl' in sessionFiles:
            self.action = "loading a past google session..."
            cookies = pickle.load(open(f'sessions/google_{str(self.email).lower()}.pkl', 'rb'))
            self.driver.get("https://myaccount.google.com")
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        else:
            self.action = 'no previous session was found...'
            time.sleep(1)
            return False

        if f"youtube_{str(self.email).lower()}.pkl" in sessionFiles:
            self.action = "loading a past youtube session..."
            cookies = pickle.load(open(f'sessions/youtube_{str(self.email).lower()}.pkl', 'rb'))
            self.driver.get("https://youtube.com")
            for cookie in cookies:
                self.driver.add_cookie(cookie)

        self.driver.get("https://mail.google.com/mail/u/0/?tab=mm")
        if "accounts.google.com" in self.driver.current_url:
            loginAttempt = self.login()
            if loginAttempt == None:
                self._safeExit(save=False)
            elif not loginAttempt:
                self._safeExit(save=False)
        else:
            self.newTab()

        return True

    def progress(self):
        while True:
            if self.action == 'quit':
                sys.exit(0)

            os.system('clear')
            sys.stdout.flush()
            logo()

            printElements = []
            printElements.append(f" | Task ID: {str(self.config['tid'])}")
            printElements.append(f" | Account: {self.email}")

            printElements.append(f" | Proxy Enabled: {str(self.config['settings']['proxy'])}")
            if self.config['settings']['proxy']:
                printElements.append(f" | Proxy: {str(self.config['proxy'])}")

            printElements.append(f" | Watch Time: {str(self.currentWatchTime)}/{str(self.maxWatchTime)} (sec)")
            printElements.append(f" | Google Searches: {str(self.completedSearches)}/{str(self.maxSearches)}")
            printElements.append(f" | News Stories: {str(self.readStories)}/{str(self.maxStories)}")
            printElements.append(f" | Translation Progress: {str(self.currentTranslations)}/{str(self.maxTranslations)}")
            printElements.append(f" | GMail Actions: {str(self.completedEmailActions)}/{str(self.maxEmailActions)}")

            printElements.append(f" | Elapsed Time: {str(time.time() - self.startTime).split('.')[0]}s\n")
            printElements.append(f" [+] Currently {self.action}")

            if self.notification != None:
                printElements.append(f" [!] {str(self.notification)}")

            sys.stdout.write(colored('\n'.join(printElements), 'red'))

            time.sleep(0.5)

    def createOpenSession(self, save=False):
        Thread(target=self.progress, daemon=True).start()
        self.createDriver()

        if not self.readCookies() or save:
            loginAttempt = self.login()
            if loginAttempt == None:
                self._safeExit(save=False)
            elif not loginAttempt:
                self._safeExit(save=False)

        if save:
            self._safeExit(save=True)

        self.action = 'running a regular browsing session...'
        input("")

    def startProcess(self):
        try:
            Thread(target=self.progress, daemon=True).start()

            self.createDriver()

            if not self.readCookies():
                loginAttempt = self.login()
                if loginAttempt == None:
                    self._safeExit(save=False)
                elif not loginAttempt:
                    self._safeExit(save=False)
        except Exception as e:
            self._safeExit(save=False)

        try:
            while True:
                if self.completedSearches >= self.maxSearches and self.currentWatchTime >= self.maxWatchTime and self.readStories >= self.maxStories and self.currentTranslations >= self.maxTranslations and self.completedEmailActions >= self.maxEmailActions:
                    break

                roller = random.randint(1, 5)
                if roller == 1 and self.completedSearches < self.maxSearches:
                    self.startSearch()
                elif roller == 2 and self.currentWatchTime < self.maxWatchTime:
                    self.startYoutube(duration=random.randint(12, self.maxWatchTime))
                elif roller == 3 and self.currentTranslations < self.maxTranslations:
                    self.startTranslating()
                elif roller == 4 and self.readStories < self.maxStories:
                    self.startNews()
                elif roller == 5 and self.completedEmailActions < self.maxEmailActions:
                    self.startEmail()
        except:
            self._safeExit(save=True)

        self._safeExit(save=True)
