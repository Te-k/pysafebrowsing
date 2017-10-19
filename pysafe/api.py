import requests
import json


class SafeBrowsingInvalidApiKey(Exception):
    def __init__(self):
        Exception.__init__(self, "Invalid API key for Google Safe Browsing")


class SafeBrowsingWeirdError(Exception):
    def __init__(self, code, status, message, details):
        self.message = "%s(%i): %s (%s)" % (
            status,
            code,
            message,
            details
        )
        Exception.__init__(self, message)


class SafeBrowsing(object):
    def __init__(self, key):
        self.api_key = key

    def lookup_urls(self, urls, platforms=["ANY_PLATFORM"]):
        data = {
            "client": {
                "clientId":      "pysafe",
                "clientVersion": "0.1"
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
                "threatEntries": [{'url': u} for u in urls]
            }
        }
        headers = {'Content-type': 'application/json'}

        r = requests.post(
                'https://safebrowsing.googleapis.com/v4/threatMatches:find',
                data=json.dumps(data),
                params={'key': self.api_key},
                headers=headers
        )
        if r.status_code == 200:
            # Return clean results
            if r.json() == {}:
                return dict([(u, {"malicious": False}) for u in urls])
            else:
                result = {}
                for url in urls:
                    # Get matches
                    matches = [match for match in r.json()['matches'] if match['threat']['url'] == url]
                    if len(matches) > 0:
                        result[url] = {
                            'malicious': True,
                            'platforms': list(set([b['platformType'] for b in matches])),
                            'threats': list(set([b['threatType'] for b in matches])),
                            'cache': min([b["cacheDuration"] for b in matches])
                        }
                    else:
                        result[url] = {"malicious": False}
                return result
        else:
            if r.status_code == 400:
                if r.json()['error']['message'] == 'API key not valid. Please pass a valid API key.':
                    raise SafeBrowsingInvalidApiKey()
                else:
                    raise SafeBrowsingWeirdError(
                        r.json()['error']['code'],
                        r.json()['error']['status'],
                        r.json()['error']['message'],
                        r.json()['error']['details']
                    )
            else:
                raise SafeBrowsingWeirdError(r.status_code, "", "", "")

    def lookup_url(self, url, platforms=["ANY_PLATFORM"]):
        """
        Online lookup of a single url
        """
        r = self.lookup_urls([url], platforms=platforms)
        return r[url]
