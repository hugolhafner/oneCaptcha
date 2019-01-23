import json, os

class Open:
    def read(self, file):
        try:
            with open(file) as this:
                if 'txt' in file.lower():
                    value = []
                    for i in this.readlines():
                        raw = i.strip().replace('\n', '').split(',')
                        for a in raw:
                            value.append(a)
                    return value

                elif 'json' in file.lower():
                    return json.load(this)
        except Exception:
            if os.path.isfile(file):
                print("Error loading the following file {}, please ensure it is properly formatted!".format(file))
            else:
                print("Error loading the following file {}, please ensure it exists in the current directory!".format(file))

            os._exit(1)

    def write(self, file, text='', method='w+'):
        try:
            with open(file, method) as this:
                if 'json' in file:
                    json.dump(text, this)
                else:
                    this.write(text)
        except Exception as e:
            print("Error loading the following file {}! {}".format(file, e))
