Extending SemRep with Dietary Supplement Terminology
==============================
Author: Jake Vasilakes (jvasilakes@gmail.com)


Overview
--------------
  1. Extend the UMLS Metathesaurus data files to include the iDISK dietary supplement (DS) ingredient terminology.
  2. Load this extended terminology (UMLS\_DS) into MetaMap using the MetaMap Datafile Builder.
  3. Link the resulting MetaMap data files into SemRep to create SemRep\_DS.
  4. Obtain a set of biomedical journal abstracts containing DS mentions using the PubMed eUtils API.
  5. Run SemRep\_DS and Vanilla SemRep on these abstracts to obtain two sets of predications, one for each system.
  6. Evaluate SemRep\_DS by
    * Determining how many new DS-related predications are found by SemRep\_DS over Vanilla.
    * Determining how many non-DS predications SemRep\_DS misses compared to Vanilla.
    * Compute the precision of the DS-related predicates found by SemRep\_DS via manual evaluation.


## Steps

### Prerequisites

#### Install iDISK
Get the latest version at https://github.com/zhang-informatics/iDISK/releases. This file assumes you're using 1.0.1.
Extract the files to `data/external/iDISK/1.0.1`.
Then install `idlib`, which contains necessary scripts for completing step 1, following https://github.com/zhang-informatics/iDISK/tree/master/lib/idlib

#### Obtain the 2006AA USABase UMLS data files.

You'll have to extract them using MetaMorphoSys. Download the files at https://www.nlm.nih.gov/research/umls/licensedcontent/umlsarchives04.html#2006AA. 
Unzip mmsys.zip and run `linux_mmsys.sh`. To replicate the USABase subset, INCLUDE all sources of levels 0 and 4, and EXCLUDE all other sources.

### Step 1. Extend the UMLS Metathesaurus data files to include the iDISK dietary supplement ingredient terminology.

Just run

```
make idisk_umls
```

### Steps 2 (load the extended terminology into MetaMap) and 3 (link the new MetaMap installation to SemRep).

See the README at `data/external/MetaMap`.

### Step 4. Obtain a set of biomedical journal abstracts

First download 100k abstracts to from PubMed to `data/raw/abstracts.ml` with

```
make get_abstracts
```

Then, split this file of 100k abstracts into 100 files of 1000 abstracts each with

```
make split_abstracts
```

This command will save the new split files in `data/raw/abstracts_split`.

This is necessary for the parallel processing done in step 5.

### Step 5. Run SemRep on the abstracts.

*The following must be run on a server.*

First install GNU parallel (http://www.gnu.org/software/parallel/) on helios.

Once `parallel` is installed, run SemRep extended with the DS terminology.

```
make run_semrep_ds
```

Run Vanilla SemRep with 

```
make run_semrep
```

*NB*: Both of the above commands will take around 10 hours to complete, depending on the number of processes you specify when invoking `parallel`
(default 10, but you can change this in the Makefile). It is extremely helpful to run these commands in a tmux shell
```
tmux new -s semrep
make run_semrep
Ctrl+b d  # disconnect from the tmux session
tmux at -t semrep  # reconnect to the tmux session.
```

### Step 6. Evaluate SemRep

You can compare the predications found by two different SemRep runs by running `python src/analysis/compare_predicates.py`.

To obtain a set of DS-related predications for manual evaluation and precision computation run

```
python src/data/sample_semrep_output.py \
	# The file to sample from.
	--semrep_output data/processed/idisk_umls.semrep.out \
	# Where to save the sample.
	--outfile data/external/evaluation/idisk_umls.semrep_sampled.out \
	# Sample all DS-related predications from 300 abstracts
	--num_abstracts 300 --ds_only \
	# Only sample predications that use one of the following predicates
	--restrict_predicates STIMULATES INTERACTS_WITH INHIBITS ADMINISTERED_TO COEXISTS_WITH COMPLICATES DIAGNOSES MANIFESTATION_OF PRECEDES PREVENTS PROCESS_OF PRODUCES TREATS USES
```

The above takes an optional `--pmid_list` argument, which allows you to specify a list of PMIDs to extract from the `--semrep_output`. This is essential for comparing the output
of two systems, such as SemRep DS and Vanilla, or two different SemRep DS versions.

The annotation guidelines, a description of the fields in the evaluation files, and example evaluation files are at `data/external/evaluation`.


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands to carry out steps 1, 4, and 5 above. See the README for instructions on the other steps.
    ├── README.md          <- The top-level README. This file.
    ├── docs               <- Various project documentation.
    ├── data
    │   ├── external       <- External data not directly produced by the pipeline
    │   │   ├── MetaMap    <- A description of the MetaMap data file builder process.
    │   │   ├── SemRepQC   <- Quality Control data for SemRep\_DS development. Useful for comparing versions without a formal evaluation.
    │   │   ├── iDISK      <- A link to the iDISK version 1.0.1, from which the DS ingredient terminology was extracted.
    │   │   └── evaluation <- Data for the evaluation of SemRep\_DS.   
    │   ├── interim        <- Empty. On helios it will contain the intermediate SemRep output.
    │   ├── processed      <- Full output of SemRep (both DS and Vanilla) on the journal abstracts goes here. scp from the correspond directory on helios.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── reports            <- Comparisons of SemRep\_DS to Vanilla.
    │   └── figures        <- Generated graphics and figures to be used in reporting. Currently empty.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.
        ├── analysis       <- Scripts to analyze data and SemRep output.
        │   └── compare_predications.py
        │
        └── data           <- Scripts to download or generate data
            ├── extend_umls_with_idisk.sh  <- Run the script which extends UMLS 2006AA with the iDISK DS ingredient terminology.
            ├── get_pubmed_abstracts.py    <- Query the PubMed eUtils API to download abstracts in MEDLINE format.
            ├── split_medline.py           <- Split a large MEDLINE file into smaller files for parallel processing. Used with models/parallel_semrep.sh
            └── sample_semrep_output.py    <- Sample predications from a large file of SemRep full-fielded output for review/evaluation/etc.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
