import re, requests, sys, argparse

class RegEx:
    def __init__(self, pattern, desc):
        self.pattern = pattern
        self.desc = desc

rgxEmail = RegEx(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", "Emails")
rgxIndPhone = r"\+?\d[\d -]{8,12}\d"
rgxPhone = RegEx(rgxIndPhone, "Phone Numbers")
rgxIP = RegEx(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "IP Addresses")
rgxWord = RegEx(r"[a-zA-Z]+", "Words")

def scrapeURL(url, rgx):
    try:
        src = requests.get(url.strip())
        for rg in rgx:
            print("[*] Scraping" + rg.desc + " form " + url.strip())
            res = set(re.findall(rg.pattern, src.text, re.I))
            for dat in res:
                print(dat)
    except Exception as err:
        print(str(err))

def scrapeFile(fle, rgx):
    try:
        with open(fle) as fh:
            for url in fh:
                scrapeURL(url, rgx)
    except Exception as err:
        print(str(err))

def main(args):
    rgx = []
    isFile = True
    if args.input.lower().startswith("http"):
        isFile = False
    if args.scrape.lower() == "e": #scrape emails
        rgx = [rgxEmail]
    elif args.scrape.lower() == "p": #scrape phone #
        rgx = [rgxPhone]
    elif args.scrape.lower() == "w": #scrape words
        rgx = [rgxWord]
    elif args.scrape.lower() == "i": #scrape IP
        rgx = [rgxIP]
    elif args.scrape.lower() == "a": #scrape everything
        rgx = [rgxEmail, rgxPhone, rgxWord, rgxIP]

    if isFile:
        scrapeFile(args.input, rgx)
    else:
        scrapeURL(args.input, rgx)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", action="store", type=str, help="The URL or file containing URLs to scrape")
    parser.add_argument("scrape", action="store", type=str, nargs="?", default="a", 
        help="e = Email, p = Phone, i = IPs, w = Words, a = All")

    if len(sys.argv[2:])==0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)
