import argparse
from tqdm import tqdm


"""
Run a comparison of the predications found by two SemRep systems.
Sorry it's all in main(). I wrote this rather quickly...
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", type=str,
                        help="""First file of SemRep results""")
    parser.add_argument("file2", type=str,
                        help="""Second file of SemRep results""")
    parser.add_argument("outfile", type=str,
                        help="""Where to save the results""")
    parser.add_argument("--cui_prefix", type=str, default=None,
                        help="Only look at CUIs with the specified prefix.")
    parser.add_argument("--ignore_predicate",
                        action="store_true", default=False,
                        help="""If specified, don't consider the predicate
                                when comparing relationships.""")
    return parser.parse_args()


def main(args):
    lines1 = (l.strip() for l in open(args.file1) if l.strip() != ''
              and not l.strip().startswith("###"))
    lines2 = (l.strip() for l in open(args.file2) if l.strip() != ''
              and not l.strip().startswith("###"))

    print("Reading input files...")
    ents1 = []
    rels1 = []
    for l1 in tqdm(lines1):
        l1 = l1.split('|')
        if l1[5] == "entity":
            ents1.append(l1)
        elif l1[5] == "relation":
            rels1.append(l1)

    ents2 = []
    rels2 = []
    for l2 in tqdm(lines2):
        l2 = l2.split('|')
        if l2[5] == "entity":
            ents2.append(l2)
        elif l2[5] == "relation":
            rels2.append(l2)
    print("Done")

    print("Converting to sets...")
    # PMID, TI/AB, SENT_INDEX, MENTION_TEXT
    ent_idxs = [1, 3, 4, 11]
    ents1_set = {tuple(l[i] for i in ent_idxs) for l in tqdm(ents1)}
    ents2_set = {tuple(l[i] for i in ent_idxs) for l in tqdm(ents2)}
    if args.ignore_predicate is True:
        # PMID, TI/AB, SENT_INDEX, SUBJECT_TEXT, OBJECT_TEXT
        rel_idxs = [1, 3, 4, 14, 34]
    else:
        # PMID, TI/AB, SENT_INDEX, SUBJECT_TEXT, PREDICATE, OBJECT_TEXT
        rel_idxs = [1, 3, 4, 14, 22, 34]
    rels1_set = {tuple(l[i] for i in rel_idxs) for l in tqdm(rels1)}
    rels2_set = {tuple(l[i] for i in rel_idxs) for l in tqdm(rels2)}
    print("Done")

    pmids = [set(), set()]

    print("Counting entities...")
    ds_ent_pmids = [set(), set()]
    ds_ents = [list(), list()]
    total_ents = [0, 0]
    found_ents = [ents1[:], ents2[:]]
    for (ei, (el, es)) in enumerate([(ents1, ents2_set), (ents2, ents1_set)]):
        for (i, e) in tqdm(enumerate(el)):
            pmid = e[1]
            pmids[ei].add(pmid)
            if e[6].startswith("DC"):  # Dietary supplement
                ds_ent_pmids[ei].add(pmid)
                ds_ents[ei].append(e)

            total_ents[ei] += 1
            ent_tuple = tuple(e[i] for i in ent_idxs)
            if ent_tuple in es:
                found_ents[ei][i].append(True)
            else:
                found_ents[ei][i].append(False)
    print("Done")

    print("Counting relations...")
    ds_rel_pmids = [set(), set()]
    ds_rels = [list(), list()]
    total_rels = [0, 0]
    found_rels = [rels1[:], rels2[:]]
    for (ri, (rl, rs)) in enumerate([(rels1, rels2_set), (rels2, rels1_set)]):
        for (i, r) in tqdm(enumerate(rl)):
            pmid = r[1]
            pmids[ri].add(pmid)
            if r[8].startswith("DC") or r[28].startswith("DC"):
                ds_rel_pmids[ri].add(pmid)
                ds_rels[ri].append(r)

            total_rels[ri] += 1
            rel_tuple = tuple(r[i] for i in rel_idxs)
            if rel_tuple in rs:
                found_rels[ri][i].append(True)
            else:
                found_rels[ri][i].append(False)
    print("Done")

    intersect_pmids = set(pmids[0]).intersection(set(pmids[1]))

    is_ds1 = "DS"
    is_ds2 = "DS"
    epmids1 = set(ds_ent_pmids[0])
    epmids2 = set(ds_ent_pmids[1])
    if len(ds_ent_pmids[0]) == 0:
        is_ds1 = "ALL"
        epmids1 = set(pmids[0])
    if len(ds_ent_pmids[1]) == 0:
        is_ds2 = "ALL"
        epmids2 = set(pmids[1])
    intersect_ent_pmids = epmids1.intersection(epmids2)

    rpmids1 = set(ds_rel_pmids[0])
    rpmids2 = set(ds_rel_pmids[1])
    if len(ds_rel_pmids[0]) == 0:
        is_ds1 = "ALL"
        rpmids1 = set(pmids[0])
    if len(ds_ent_pmids[1]) == 0:
        is_ds2 = "ALL"
        rpmids2 = set(pmids[1])
    intersect_rel_pmids = rpmids1.intersection(rpmids2)

    eset1 = {tuple(e[i] for i in ent_idxs) for e in ds_ents[0]}
    eset2 = {tuple(e[i] for i in ent_idxs) for e in ds_ents[1]}
    if len(ds_ents[0]) == 0:
        is_ds1 = "ALL"
        eset1 = ents1_set
    if len(ds_ents[1]) == 0:
        is_ds2 = "ALL"
        eset2 = ents2_set
    intersect_ents = eset1.intersection(eset2)

    rset1 = {tuple(r[i] for i in rel_idxs) for r in ds_rels[0]}
    rset2 = {tuple(r[i] for i in rel_idxs) for r in ds_rels[1]}
    if len(ds_rels[0]) == 0:
        is_ds1 = "ALL"
        rset1 = rels1_set
    if len(ds_rels[1]) == 0:
        is_ds2 = "ALL"
        rset2 = rels2_set
    intersect_rels = rset1.intersection(rset2)

    for (i, fname) in enumerate([args.file1, args.file2]):
        print(f"FILE {i+1}: {fname}")
        print(f"  PMIDs: {len(pmids[i])}")
        print(f"  PMIDs with DS mentions: {len(ds_ent_pmids[i])}")
        print(f"  PMIDs with DS relations: {len(ds_rel_pmids[i])}")

        print(f"  All Mentions: {total_ents[i]}")
        print(f"  DS Mentions: {len(ds_ents[i])}")

        print(f"  All Relations: {total_rels[i]}")
        print(f"  DS Relations: {len(ds_rels[i])}")

    print()
    print("INTERSECTIONS")
    print(f"  PMIDs, Files 1v2: {len(intersect_pmids)}")
    print(f"  Mention PMIDs, Files 1({is_ds1}) v 2({is_ds2}): {len(intersect_ent_pmids)}")  # noqa
    print(f"  Relation PMIDs, Files 1({is_ds1}) v 2({is_ds2}): {len(intersect_rel_pmids)}")  # noqa
    print(f"  Mentions, Files 1({is_ds1}) v 2({is_ds2}): {len(intersect_ents)}")  # noqa
    print(f"  Relations, Files 1({is_ds1}) v 2({is_ds2}): {len(intersect_rels)}")  # noqa


if __name__ == "__main__":
    args = parse_args()
    main(args)
