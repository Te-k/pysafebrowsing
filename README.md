# Pysafebrowsing

[![PyPI](https://img.shields.io/pypi/v/pysafebrowsing)](https://pypi.org/project/pysafebrowsing/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pysafebrowsing)](https://pypistats.org/packages/pysafebrowsing) [![PyPI - License](https://img.shields.io/pypi/l/pysafebrowsing)](LICENSE) [![GitHub issues](https://img.shields.io/github/issues/te-k/pysafebrowsing)](https://github.com/Te-k/pysafebrowsing/issues)

Limited python3 library for [Google Safe Browsing API v4](https://developers.google.com/safe-browsing/v4/). For now, only the online lookup is developed. Check [here](https://developers.google.com/safe-browsing/v4/get-started) to get an API key.

To install, you can just install it from [pypi](https://pypi.org/project/pysafebrowsing) with `pip install pysafebrowsing`, or download the code with `git clone https://github.com/Te-k/pysafebrowsing.git` and then `pip install .`

## Library

```python
from pysafebrowsing import SafeBrowsing
s = SafeBrowsing(KEY)
r = s.lookup_urls(['http://malware.testing.google.test/testing/malware/'])
print(r)
> {'http://malware.testing.google.test/testing/malware/': {'platforms': ['ANY_PLATFORM'], 'threats': ['MALWARE', 'SOCIAL_ENGINEERING'], 'malicious': True, 'cache': '300s'}}
```

## CLI

```
$ safebrowsing config --key dfdsfdsfds
In /home/user/.config/safebrowsing:
[SafeBrowsing]
key = dfdsfdsfds

$ safebrowsing url http://malware.testing.google.test/testing/malware/
Malicious: Yes
Platforms: ANY_PLATFORM
Threats: SOCIAL_ENGINEERING, MALWARE

$ safebrowsing url https://github.com/
Malicious: No

$ safebrowsing file testlist.txt
http://malware.testing.google.test/testing/malware/     Malicious
http://twitter.com/     Ok
https://github.com/     Ok
http://www.google.com/  Ok
http://www.yahoo.com/   Ok
http://ianfette.org     Malicious
```

## License

This code is published under MIT license: do whatever you want with it, but don't blame me if it fails ;)
