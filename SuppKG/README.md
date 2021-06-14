# SuppKG
---

SuppKG was generated using SemRepDS on 600k PubMed abstracts to find semantic triples involving dietary supplements found in the UMLS+iDISK [@rizvi_idisk_2020]. There are 56,635 nodes and 595,222 directed edges. Each node is identified by the CUI and within each node is the semantic type of the concept and the individual terms extracted from the abstracts. Each edge is one of 31 predicates and within each edge is the sentence the semantic triple (node, edge, node) was extracted from, the PMID of the abstract the sentence can be found in, and the confidence score of our BERT filtering model. If one triple was found in multiple sentences, each sentence, PMID, and confidence score is included in the edge attributes.
<br>
## Files
supp_kg.gpickle.bz2 was generated using the NetworkX (2.5) Python package.
<br>
TODO:
1) Add SuppKG neo4j
2) Add citations
3) Add examples


## Citations

@article{rizvi_idisk_2020,
	title = {{iDISK}: the integrated {DIetary} {Supplements} {Knowledge} base},
	volume = {27},
	issn = {1527-974X},
	shorttitle = {{iDISK}},
	url = {https://academic.oup.com/jamia/article/27/4/539/5740032},
	doi = {10.1093/jamia/ocz216},
	language = {en},
	number = {4},
	urldate = {2021-03-12},
	journal = {Journal of the American Medical Informatics Association},
	author = {Rizvi, Rubina F and Vasilakes, Jake and Adam, Terrence J and Melton, Genevieve B and Bishop, Jeffrey R and Bian, Jiang and Tao, Cui and Zhang, Rui},
	month = apr,
	year = {2020},
	pages = {539--548},
	file = {Full Text:/Users/schut184/Zotero/storage/DK6LNRQD/Rizvi et al. - 2020 - iDISK the integrated DIetary Supplements Knowledg.pdf:application/pdf}
}
