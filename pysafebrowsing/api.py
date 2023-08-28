import json

import requests

from .about import __version__


class SafeBrowsingException(Exception):
    pass


class SafeBrowsingInvalidApiKey(SafeBrowsingException):
    def __init__(self):
        Exception.__init__(self, "Invalid API key for Google Safe Browsing")


class SafeBrowsingPermissionDenied(SafeBrowsingException):
    def __init__(self, detail):
        Exception.__init__(self, detail)


class SafeBrowsingWeirdError(SafeBrowsingException):
    def __init__(self, code, status, message):
        self.message = "%s(%i): %s" % (
            status,
            code,
            message
        )
        Exception.__init__(self, message)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class SafeBrowsing(object):
    def __init__(self, key,
                 api_url='https://safebrowsing.googleapis.com/v4/threatMatches:find'):
        self.api_key = key
        self.api_url = api_url

    def lookup_urls(self, urls, platforms=["ANY_PLATFORM"]):
        results = {}
        for urll in chunks(urls, 25):
            data = {
                "client": {
                    "clientId": "pysafebrowsing",
                    "clientVersion": __version__
                },
                "threatInfo": {
                    "threatTypes":
                        [
                            "MALWARE",
                            "SOCIAL_ENGINEERING",
                            "THREAT_TYPE_UNSPECIFIED",
                            "UNWANTED_SOFTWARE",
                            "POTENTIALLY_HARMFUL_APPLICATION"
                        ],
                    "platformTypes": platforms,
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{'url': u} for u in urll]
                }
            }
            headers = {'Content-type': 'application/json'}

            r = requests.post(
                self.api_url,
                data=json.dumps(data),
                params={'key': self.api_key},
                headers=headers
            )
            if r.status_code == 200:
                # Return clean results
                if r.json() == {}:

                    results.update(dict([(u, {"malicious": False}) for u in urll]))
                else:
                    for url in urll:
                        # Get matches
                        matches = [match for match in r.json()['matches'] if match['threat']['url'] == url]
                        if len(matches) > 0:
                            results[url] = {
                                'malicious': True,
                                'platforms': list(set([b['platformType'] for b in matches])),
                                'threats': list(set([b['threatType'] for b in matches])),
                                'cache': min([b["cacheDuration"] for b in matches])
                            }
                        else:
                            results[url] = {"malicious": False}
            else:
                if r.status_code == 400:
                    print(r.json())
                    if r.json()['error']['message'] == 'API key not valid. Please pass a valid API key.':
                        raise SafeBrowsingInvalidApiKey()
                    else:
                        raise SafeBrowsingWeirdError(
                            r.json()['error']['code'],
                            r.json()['error']['status'],
                            r.json()['error']['message'],
                        )
                elif r.status_code == 403:
                    raise SafeBrowsingPermissionDenied(r.json()['error']['message'])
                else:
                    raise SafeBrowsingWeirdError(r.status_code, "", "", "")
        return results

    def lookup_url(self, url, platforms=["ANY_PLATFORM"]):
        """
        Online lookup of a single url
        """
        r = self.lookup_urls([url], platforms=platforms)
        return r[url]
