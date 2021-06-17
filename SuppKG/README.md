# SuppKG
---

SuppKG was generated using SemRepDS on 600k PubMed abstracts to find semantic triples involving dietary supplements found in the UMLS+iDISK. There are 56,635 nodes and 595,222 directed edges. Each node is identified by the CUI and within each node is the semantic type of the concept and the individual terms extracted from the abstracts. Each edge is one of 31 predicates and within each edge is the sentence the semantic triple (node, edge, node) was extracted from, the PMID of the abstract the sentence can be found in, and the confidence score of our BERT filtering model. If one triple was found in multiple sentences, each sentence, PMID, and confidence score is included in the edge attributes.
<br>
## Files
* supp_kg.gpickle.bz2 was generated using the NetworkX (2.5) Python package. Python 3.8 was used to generate the file which uses Pickle protocol 5. Opening the file using networkx.readwrite.gpickle.read_gpickle() will require using Python 3.8.
* supp_kg.json.tar.bz2 can be decompressed and loaded using json.load() and passing the resulting dictionary to networkx.readwrite.json_graph.node_link_graph()

<br><br>
TODO:
1) Add SuppKG neo4j
2) Add citations
3) Add examples


## Citations
