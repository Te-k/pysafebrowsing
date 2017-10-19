# Pysafe

Limited python3 library for [Google Safe Browsing API v4](https://developers.google.com/safe-browsing/v4/). For now, only the online lookup is developed. Check [here](https://developers.google.com/safe-browsing/v4/get-started) to get am API key. To install, download the library and do `python setup.py install`, or add `git+https://github.com/Te-k/pysafe.git` to your requirements.txt.

## Library

```python
from pysafe import SafeBrowsing
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
```
