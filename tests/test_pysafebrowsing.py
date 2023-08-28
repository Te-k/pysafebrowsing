import configparser
import os

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
        assert res["malicious"] is False

    def test_bad(self):
        conf = load_config()
        sb = SafeBrowsing(conf['SafeBrowsing']['key'])
        res = sb.lookup_url("http://malware.testing.google.test/testing/malware/")
        assert res["malicious"] is True

    def test_chunk(self):
        conf = load_config()
        sb = SafeBrowsing(conf['SafeBrowsing']['key'])
        testlist = ["https://google.com/"]*25
        testlist.append("http://malware.testing.google.test/testing/malware/")
        res = sb.lookup_urls(testlist)
        assert "http://malware.testing.google.test/testing/malware/" in res
        assert res["http://malware.testing.google.test/testing/malware/"]["malicious"] is True
        assert "https://google.com/" in res
        assert res["https://google.com/"]["malicious"] is False
