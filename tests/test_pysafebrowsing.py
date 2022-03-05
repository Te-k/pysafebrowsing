import os
import configparser
from pysafebrowsing import SafeBrowsing

def load_config():
    configfile = os.path.expanduser('~/.config/safebrowsing')
    if not os.path.isfile(configfile):
        return {}
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


class TestPySafeBrowsing:
    def test_not_bad(self):
        conf = load_config()
        sb = SafeBrowsing(conf['SafeBrowsing']['key'])
        res = sb.lookup_url("https://google.com")
        assert res["malicious"] == False

    def test_bad(self):
        conf = load_config()
        sb = SafeBrowsing(conf['SafeBrowsing']['key'])
        res = sb.lookup_url("http://malware.testing.google.test/testing/malware/")
        assert res["malicious"] == True
