import re,requests,sys,argparse

class RegEx:
    def __init__(self,pattern,desc):
        self.pattern = pattern
        self.desc = desc

rgxEmail = RegEx(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", "Emails")
rgxPhone = RegEx(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "Phone Numbers")
rgxIP = RegEx(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "IP Addresses")
rgxWord = RegEx(r"[a-zA-Z]+", "Words")

def scrapeUrl(url,rgx):
    try:
        src = requests.get(url.strip())
        for rg in rgx:
            print("[*] Scrapping "+rg.desc+" from "+url.strip())
            res = set(re.findall(rg.pattern,src,text,re.I))
            for dat in res:
                print(dat)
    except Exception as err:
        print(str(err))

def scrapeFile(fle,rgx):
    try:
        with open(fle) as fh:
            for url in fh:
                scrapeUrl(url,rgx)
    except Exception as err:
        print(str(err))

def main(args):
    rgx = []
    isFile = True
    if args.input.lower().startswith("http"):
        isFile = false
    elif args.scrape.lower() == "e":
        rgx = [rgxEmail]
    elif args.scrape.lower() == "p":
        rgx = [rgxPhone]
    elif args.scrape.lower() == "w":
        rgx = [rgxWord]
    elif args.scrape.lower() == "i":
        rgx = [rgxIP]
    elif args.scrape.lower() == "a":
        rgx = [rgxPhone,rgxIP,rgxWord,rgxEmail]

    if isFile:
        scrapeFile(args.input,rgx)
    else:
        scrapeUrl(args.input,rgx)


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


