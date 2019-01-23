import time, inquirer
from threading import Thread
from classes.utils import *
from classes.logger import Logger
from classes.openfile import Open
from modules.account import Account

if __name__ == '__main__':
    log = Logger("M").log
    read = Open().read
    logo()

    git = Github()
    git.printCommit(amount=1)

    log("Loading oneCaptcha settings...\n", 'note')
    accounts = read('config/accounts.json')

    for account in accounts:
        questions = [
            inquirer.List('selection', message=f"Action choice for {str(account['account']).split(':')[0]}",
                          choices=['Start oneCaptcha Engine', 'Regular Browsing Session', 'Update Cookie Session'],
                          ),
        ]

        answers = inquirer.prompt(questions)
        acc = Account(account)

        if answers['selection'] == 'Start oneCaptcha Engine':
            Thread(target=acc.startProcess, daemon=True).start()
        elif answers['selection'] == "Regular Browsing Session":
            Thread(target=acc.createOpenSession, daemon=True).start()
        elif answers['selection'] == "Update Cookie Session":
            Thread(target=acc.createOpenSession, kwargs={'save': True}, daemon=True).start()
        else:
            Thread(target=acc.startProcess, daemon=True).start()

    while True:
        time.sleep(1000)