import argparse
import configparser
import json
import os
import sys

from .api import (SafeBrowsing, SafeBrowsingInvalidApiKey,
                  SafeBrowsingWeirdError)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    parser = argparse.ArgumentParser(description='Request SpyOnWeb')
    subparsers = parser.add_subparsers(help='Commands')
    parser_a = subparsers.add_parser('config', help='Configuration of the tool')
    parser_a.add_argument('--key', '-k', help='Configure the tool')
    parser_a.set_defaults(which='config')
    parser_b = subparsers.add_parser('url', help='Query an URL')
    parser_b.add_argument('URL', help='URL to be requested')
    parser_b.add_argument('--json', '-j', action='store_true', help='Show raw json')
    parser_b.set_defaults(which='url')
    parser_c = subparsers.add_parser('file', help='Check domains or urls from a file')
    parser_c.add_argument('FILE', help='File path')
    parser_c.add_argument(
        '--format', '-f', help='File path',
        choices=["json", "csv", "txt"], default="txt")
    parser_c.set_defaults(which='file')
    args = parser.parse_args()

    configfile = os.path.expanduser('~/.config/safebrowsing')

    if hasattr(args, 'which'):
        if args.which == 'config':
            if args.key:
                config = configparser.ConfigParser()
                config['SafeBrowsing'] = {'key': args.key}
                with open(configfile, 'w') as cf:
                    config.write(cf)
            if os.path.isfile(configfile):
                print('In %s:' % configfile)
                with open(configfile, 'r') as cf:
                    print(cf.read())
            else:
                print('No configuration file, please create one with config --key')
        else:
            if not os.path.isfile(configfile):
                print('No configuration file, please create one with config --key')
                sys.exit(1)
            config = configparser.ConfigParser()
            config.read(configfile)
            sb = SafeBrowsing(config['SafeBrowsing']['key'])
            if args.which == 'url':
                try:
                    if args.URL.startswith("http"):
                        res = sb.lookup_url(args.URL)
                    else:
                        res = sb.lookup_url("http://" + args.URL + "/")
                except SafeBrowsingInvalidApiKey:
                    print("Invalid API key!")
                    sys.exit(1)
                except SafeBrowsingWeirdError:
                    print("Weird Error!")
                    sys.exit(1)
                else:
                    if args.json:
                        print(json.dumps(res, sort_keys=True, indent=4))
                    else:
                        if res["malicious"]:
                            print("Malicious: Yes")
                            print("Platforms: %s" % ", ".join(res["platforms"]))
                            print("Threats: %s" % ", ".join(res["threats"]))
                        else:
                            print("Malicious: No")
            elif args.which == 'file':
                with open(args.FILE, 'r') as f:
                    data = f.read()
                domains = set([d.strip() for d in data.split()])
                for chunk in chunks(list(domains), 40):
                    res = sb.lookup_urls(chunk)
                    if args.format == "txt":
                        for domain in res:
                            if res[domain]["malicious"]:
                                print("%s\tMalicious" % domain)
                            else:
                                print("%s\tOk" % domain)
                    elif args.format == "json":
                        print(json.dumps(res, sort_keys=True, indent=4))
                    else:
                        print("Url|Malicious|Threat|Platform")
                        for domain in res:
                            if res[domain]["malicious"]:
                                print("{}|{}|{}|{}".format(
                                    domain,
                                    "Yes",
                                    ",".join(res[domain]["threats"]),
                                    ",".join(res[domain]["platforms"])
                                ))
                            else:
                                print("{}|No||".format(domain))
            else:
                parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
