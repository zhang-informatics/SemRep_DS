import argparse
import csv
import sys
from collections import defaultdict

"""
Samples the output of SemRep for a set of abstracts for manual review.
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--semrep_output", type=str, required=True,
                        help="""File containing full-fielded (-F)
                                SemRep output.""")
    parser.add_argument("--outfile", type=str, required=True,
                        help="""Where to save the sampled output.""")
    parser.add_argument("--num_abstracts", type=int, default=10,
                        help="""The number of abstracts to sample.""")
    parser.add_argument("--pmid_list", type=str, default=None,
                        help="""If specified, get all SemRep output
                                for these PMIDs, even if no relations
                                were found.""")
    parser.add_argument("--ds_only", action="store_true", default=False,
                        help="""Only return abstracts/predications with
                                a dietary supplement (CUI prefix 'DC')
                                in the subject and/or object position.""")
    parser.add_argument("--restrict_predicates", type=str, nargs='*',
                        help="""Only return predications that have one
                                of the provided predicates.""")
    return parser.parse_args()


def main(args):
    csv.field_size_limit(sys.maxsize)
    if args.pmid_list is not None:
        keep_pmids = [l.strip() for l in open(args.pmid_list, 'r')]
        num_abstracts = len(keep_pmids)
    else:
        keep_pmids = None
        num_abstracts = args.num_abstracts
    keep_predicates = None
    if len(args.restrict_predicates) > 0:
        keep_predicates = [p.upper() for p in args.restrict_predicates]
    # sent is unique tuple of (PMID, ti/ab, sentence_number)
    sent2text = {}
    sent2rels = defaultdict(list)
    abstracts_sampled = set()
    rel_columns = [5, 8, 9, 10, 11, 14, 17, 22, 28, 29, 30, 31, 34, 37]
    with open(args.semrep_output, 'r') as inF:
        reader = csv.reader(inF, delimiter='|')

        relation_found = defaultdict(bool)
        for line in reader:
            if len(abstracts_sampled) == num_abstracts:
                break
            if not line or line[0].startswith("###"):
                continue
            if line[5] not in ["text", "relation"]:
                continue
            sent = (line[1], line[3], line[4])
            pmid = line[1]
            if keep_pmids is not None and pmid not in keep_pmids:
                continue
            if line[5] == "text":
                row = ["text"] + [line[c] for c in [1, 2, 3, 4, 8]]
                sent2text[sent] = '|'.join(row)
            elif line[5] == "relation":
                if keep_predicates is not None and line[22] not in keep_predicates:  # noqa
                    continue
                if args.ds_only is True:
                    if not line[8].startswith("DC") and not line[28].startswith("DC"):  # noqa
                        continue
                row = [line[c] for c in rel_columns]
                sent2rels[sent].append('|'.join(row))
                relation_found[sent] = True
                abstracts_sampled.add(pmid)

    with open(args.outfile, 'w') as outF:
        header = "Text Fields: PMID|SUBSECTION|TItle/ABstract|SENT_NUM|TEXT"  # noqa
        header2 = "Relation Fields: SUBJ_CUI|SUBJ_NAME|SUBJ_SEMTYPES|SUBJ_ST_USED|SUBJ_TEXT|SUBJ_NEG|PREDICATE|OBJ_CUI|OBJ_NAME|OBJ_SEMTYPES|OBJ_ST_USED|OBJ_TEXT|OBJ_NEG"  # noqa
        header3 = "See README for field descriptions."
        outF.write(f"{header}\n{header2}\n{header3}\n\n")
        current_pmid = None
        for sent, text in sent2text.items():
            if relation_found[sent] is False:
                continue
            pmid = sent[0]
            if pmid != current_pmid:
                if current_pmid is not None:
                    outF.write(f"======= END {current_pmid} =======\n\n")
                outF.write(f"======= START {pmid} =======")
                current_pmid = pmid
            text = sent2text[sent]
            outF.write('\n' + text + '\n')
            for rel in sent2rels[sent]:
                outF.write(rel + '\n')
        outF.write(f"======= END {current_pmid} =======\n\n")


if __name__ == "__main__":
    args = parse_args()
    main(args)
