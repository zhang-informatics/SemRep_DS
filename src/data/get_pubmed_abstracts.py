import argparse
import requests

"""
Queries the eUtils API for all journal article abstracts published on PubMed
between 2018 and the present day.
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outfile", type=str, required=True,
                        help="""Where to save the query result.""")
    parser.add_argument("--num_pmids", type=int, default=10,
                        help="""Maximum number of PMIDs to get.""")
    return parser.parse_args()


def main(args):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    util = "esearch.fcgi"

    params = {"db": "pubmed",
              "mindate": 2018,
              "maxdate": 3000,
              "term": "journal article[Publication Type]",
              "rettype": "uilist",
              "retmode": "json",
              "usehistory": 'y'}
    url = base_url + util
    r = requests.get(url, params=params)
    print(r.url)
    r.raise_for_status()
    data = r.json()
    print(data)
    input()
    webenv = data["esearchresult"]["webenv"]
    query_key = data["esearchresult"]["querykey"]

    N = 0
    for (retstart, retend) in chunker(args.num_pmids):
        # Get the PMIDs of articles matching this query.
        if retend > args.num_pmids:
            retend = args.num_pmids
        chunksize = retend - retstart
        print(f"{N} ({args.num_pmids})\r", end='', flush=True)
        # Get the MEDLINE formatted abstracts of the PMIDs returned above.
        util = "efetch.fcgi"
        params = {"db": "pubmed",
                  "retstart": retstart,
                  "retend": retend,
                  "retmax": chunksize,
                  "retmode": "text",
                  "rettype": "medline",
                  "query_key": query_key,
                  "WebEnv": webenv}
        url = base_url + util
        r = requests.get(url, params=params)

        mode = 'a'
        if retstart == 0:
            mode = 'w'
        with open(args.outfile, mode) as outF:
            outF.write(r.text)
        N += chunksize


def chunker(N):
    n = 0
    while n <= N:
        yield (n, n + 1000)
        n += 1000


if __name__ == "__main__":
    args = parse_args()
    main(args)
