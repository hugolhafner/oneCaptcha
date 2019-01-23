import random

class Manager:
    def __init__(self, proxy_list):
        self.proxies = self.format(proxy_list)
        self.i = 0

    def format(self, proxy_list):
        temp = []
        for proxy in proxy_list:
            try:
                proxytest = proxy.split(":")[2]
                userpass = True
            except IndexError:
                userpass = False
            if userpass == False:
                proxyedit = proxy
            if userpass == True:
                ip = proxy.split(":")[0]
                port = proxy.split(":")[1]
                userpassproxy = ip + ':' + port
                proxyedit = userpassproxy
                proxyuser = proxy.split(":")[2]
                proxyuser = proxyuser.rstrip()
                proxypass = proxy.split(":")[3]
                proxyuser = proxyuser.rstrip()
            if userpass == True:
                proxies = {'http': 'http://' + proxyuser + ':' + proxypass + '@' + userpassproxy,
                           'https': 'https://' + proxyuser + ':' + proxypass + '@' + userpassproxy}
            if userpass == False:
                proxies = {'http': 'http://' + proxy,
                           'https': 'https://' + proxy}

            temp.append(proxies)
        return temp

    def get_proxy(self):
        if (len(self.proxies) == 0):
            return None

        if self.i >= len(self.proxies):
            self.i = 0

        proxy = self.proxies[self.i]
        self.i += 1
        return proxy
