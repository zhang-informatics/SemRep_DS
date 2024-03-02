# SuppKG v2

SuppKG was recently reconstructed using additional abstracts published since the original pull in 2021 to account for updates to the literature. The same process as is described in the paper is followed for the construction of v2. There are some structural changes to the data that were made as a mix of necessity and convenience. The data can be loaded using NetworkX and the function `nx.read_edgelist(suppkg_v2.edgelist)` which will return a `nx.MultiDiGraph` object with 57,944 nodes and 1,321,374 edges.

Node structure:
```
id: str
    concept: set[str]
    semtypes: set[str]
```
Where the `id` is the concept CUI. A node can be accessed using `G.nodes()['C0005507']`

Edge structure:
```
id: int
    ${predicate}: str
```
Where id is an integer indexing the edges between the pair of nodes. PMIDs were not included due to changes in the data preprocessing in our system to speed up the process of running SemRepDS on tens of thousands of abstracts. The confidence scores from our BERT model were also omitted to reduce the memory footprint along with the tuid.

# SuppKG
---

SuppKG was generated using SemRepDS on 600k PubMed abstracts to find semantic triples involving dietary supplements found in the UMLS+iDISK. There are 56,635 nodes and 595,222 directed edges. Each node is identified by the CUI and within each node is the semantic type of the concept and the individual terms extracted from the abstracts. Each edge is one of 31 predicates and within each edge is the sentence the semantic triple (node, edge, node) was extracted from, the PMID of the abstract the sentence can be found in, and the confidence score of our BERT filtering model. If one triple was found in multiple sentences, each sentence, PMID, and confidence score is included in the edge attributes.

<br>
## Files
* supp_kg.gpickle.bz2 was generated using the NetworkX (2.5) Python package. Python 3.8 was used to generate the file which uses Pickle protocol 5. Opening the file using networkx.readwrite.gpickle.read_gpickle() will require using Python 3.8.
* supp_kg.json.tar.bz2 can be decompressed and loaded using json.load() and passing the resulting dictionary to networkx.readwrite.json_graph.node_link_graph()

