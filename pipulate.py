from urllib.parse import urlparse, urljoin

def links(soup, url):
    """Return on-site links from page duplicates removed."""
    parts = urlparse(url)
    homepage = f"{parts.scheme}://{parts.netloc}/"
    ahrefs = soup.find_all("a")
    seen = set()
    for link in ahrefs:
        if "href" in link.attrs:
            href = link.attrs["href"]
            # Skip kooky protocols like email
            if ":" in href and "//" not in href:
                continue
            # Convert relative links to absolute
            if "://" not in href:
                href = urljoin(homepage, href)
            # Convert root slash to homepage
            if href == "/":
                href = homepage
            # Strip stuff after hash (not formal part of URL)
            if "#" in href:
                href = href[: href.index("#")]
            # Remove dupes and offsite links
            if href[: len(homepage)] == homepage:
                seen.add(href)
    return seen
