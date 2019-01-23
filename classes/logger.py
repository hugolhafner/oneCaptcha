import string
from datetime import datetime
from termcolor import colored

class Logger:
    def __init__(self, tid, logFile=None, debugMode=False):
        self.format = '%H:%M:%S'
        self.tid = str(tid)
        self.logFile = logFile
        self.debugMode = debugMode

    def log(self, text, color=None, file=None, debug=None):
        timestamp = '[' + datetime.now().strftime(self.format) + ']'
        timestamp_colour = colored(timestamp, "yellow")

        if file is not None:
            self.logToFile(file, text, timestamp)
        if self.logFile is not None:
            self.logToFile(self.logFile, text, timestamp)

        if color is not None:
            text = self.getColor(text, color)

            if color == 'debug':
                if (debug != None) or (self.debugMode != None):
                    if (debug == True) or (self.debugMode == True):
                        print('{} : Task [{}] : {}'.format(timestamp_colour, self.tid, text))
                    else:
                        pass
            else:
                print('{} : Task [{}] : {}'.format(timestamp_colour, self.tid, text))
        else:
            print('{} : Task [{}] : {}'.format(timestamp_colour, self.tid, text))

    def logToFile(self, file, text, timestamp):
        printable = set(string.printable)
        text = ''.join(filter(lambda x: x in printable, text))

        try:
            with open(file, 'a+') as txt:
                txt.write('{} : Task [{}] : {}\n'.format(timestamp, self.tid, text))
        except Exception as e:
            print('ERROR: problem writing to file: {}'.format(str(e)))

    def getColor(self, text, color):
        try:
            status = {
                'success': "[{}] ".format(colored('✓', 'green')),
                'error': "[{}] ".format(colored('✗', 'red')),
                'debug': "[{}] ".format(colored('*', 'magenta')),
                'note': "[{}] ".format(colored('#', 'yellow'))
            }
            return status[color.lower()] + text
        except Exception as e:
            try:
                return colored(text, color)
            except Exception as e:
                print("WARNING: Unrecognized Color! {}".format(str(color)))