# file: pwgame.py
import config
import re
import readline
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup as bsoup
from sqlitedict import SqliteDict as sqldict

responsedb = f"{config.name}/responses.db"
keywordsdb = f"{config.name}/keywords.db"
seenurlsdb = f"{config.name}/seenurls.db"


def input_with_prefill(prefill):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input()
    finally:
        readline.set_startup_hook()


pattern = "( \| | - | & )"


def kwclean(s):
    s = s.replace(" and ", " ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(pattern, ", ", s)
    kwlist = s.split(",")
    kwlist = [x.strip() for x in kwlist]
    return kwlist


seen_urls = set()
if Path(seenurlsdb).is_file():
    with sqldict(seenurlsdb) as db:
        for url in db:
            seen_urls.add(url)

seen = set()
if Path(keywordsdb).is_file():
    with sqldict(keywordsdb) as db:
        for kw in db:
            seen.add(kw.lower())

with sqldict(responsedb) as db:
    for numpages, url in enumerate(db):
        ...

countdown = numpages
print(countdown)

with sqldict(responsedb) as db:
    for i, url in enumerate(db):
        print(countdown - i)
        if url not in seen_urls:
            response = db[url]
            soup = bsoup(response.text, "html.parser")
            title = soup.title.string.strip()
            title = ", ".join(kwclean(title))
            before_kws = kwclean(title)
            after_kws = []
            counter = Counter()
            for kw in before_kws:
                kwlow = kw.lower()
                if kwlow not in seen:
                    after_kws.append(kw)
                words = kw.split(" ")
                for word in words:
                    counter[word] += 1
            maxval = max(counter.values())
            maxlabel = max(counter, key=counter.get)
            mod_kws = []
            for j, kw in enumerate(after_kws):
                words = kw.split()
                if j == 0:
                    first = None
                    if len(words) > 1:
                        first = words[0]
                if len(words) == 1:
                    if maxval > 1:
                        kw = f"{maxlabel} {kw}"
                    elif first:
                        kw = f"{first} {kw}"
                chops = ["More"]
                for chop in chops:
                    if kw[: len(f"{chop} ")].lower() == f"{chop} ".lower():
                        kw = kw[len(f"{chop} ") :]
                mod_kws.append(kw)
            mod_kws = [x for x in mod_kws if x.lower() not in seen]
            kw_str = ", ".join(mod_kws)
            if not kw_str:
                continue
            collect = input_with_prefill(kw_str)
            print(collect)
            collect_list = collect.split(",")
            collect_list = [x.strip() for x in collect_list]
            with sqldict(keywordsdb) as db2:
                for kw in collect_list:
                    if kw and kw not in seen:
                        db2[kw] = url
                        seen.add(kw.lower())
                db2.commit()
            with sqldict(seenurlsdb) as db2:
                db2[url] = None
                db2.commit()
