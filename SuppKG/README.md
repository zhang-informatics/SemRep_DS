# SuppKG
---

SuppKG was generated using SemRepDS on 600k PubMed abstracts to find semantic triples involving dietary supplements found in the UMLS+iDISK. There are 56,635 nodes and 595,222 directed edges. Each node is identified by the CUI and within each node is the semantic type of the concept and the individual terms extracted from the abstracts. Each edge is one of 31 predicates and within each edge is the sentence the semantic triple (node, edge, node) was extracted from, the PMID of the abstract the sentence can be found in, and the confidence score of our BERT filtering model. If one triple was found in multiple sentences, each sentence, PMID, and confidence score is included in the edge attributes.
<br>
supp_kg.gpickle.bz2 was generated using the NetworkX (2.5) Python package.
<br>
TODO:
1) Add SuppKG neo4j
2) Add citations
3) Add examples
