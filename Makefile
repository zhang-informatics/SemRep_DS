.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = dsi
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif


#################################################################################
# PROJECT GLOBALS                                                               #
#################################################################################
MTH_YEAR=2006
MTH_VERSION=2006AA
MTH_DIR=/Users/vasil024/tools/Metathesaurus/2006AA/2006AA_USAbase/
# Set to path on helios
SEMREP_BIN=/home/vasil024/SemRep/public_semrep/bin/semrep.v1.8
# Number of processes to use when running SemRep.
NUM_PROC=10

#################################################################################
# PROJECT SETUP COMMANDS                                                        #
#################################################################################

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Step 1: Build UMLS+iDISK extension
idisk_umls:
	bash src/data/extend_umls_with_idisk.sh data/external/iDISK/1.0.1/ \
	  				        $(MTH_VERSION) \
					        $(MTH_DIR)
	@echo "Extended UMLS data files are at data/external/iDISK/1.0.1/build/UMLS/${MTH_VERSION}"
	@echo "Go to data/external/MetaMap for instructions on loading these files using the MetaMap Datafile Builder (Step 2) and linking these files to SemRep (Step 3)." 


## Step 4a. Obtain a set of biomedical journal abstracts containing DS mentions using the PubMed eUtils API.
get_abstracts:
	$(PYTHON_INTERPRETER) src/data/get_pubmed_abstracts.py \
			      --outfile data/raw/abstracts.ml \
			      --num_pmids 1000000

# Step 4b. Create 100 files of 1000 abstracts each for a total of 100k abstracts.
split_abstracts:
	mkdir -p data/raw/abstracts_split
	$(PYTHON_INTERPRETER) src/data/split_medline.py \
			      -N 1000 -M 100 \
			      data/raw/abstracts.ml \
			      data/raw/abstracts_split
	zip -r data/raw/abstracts.ml.100k.zip data/raw/abstracts_split
	@echo "Done splitting abstracts. To run SemRep on the abstracts, scp data/raw/abstracts.ml.100k.zip up to helios.ahc.umn.edu, ssh to the same, unzip it, and run 'make run_semrep*' commands below."


## Step 5. Run SemRep_DS and Vanilla SemRep on these abstracts to obtain two sets of predications.
run_semrep:
	@echo "It is highly recommended that you run this in a tmux shell, as it will take a long time to complete and you'll want to monitor progress by the output files. Sleeping for 5 seconds..."
	@sleep 5
	# This will run NUM_PROC SemRep instances in parallel.
	find data/raw/abstracts_split/ -name "*.txt" -type f | parallel --bar --max-procs $(NUM_PROC) $(SEMREP_BIN) -F -Z 2006 -L 2006AA -V USAbase {} {}.semrep_usabase.out '&>' {}.semrep_usabase.out.log

run_semrep_ds:
	@echo "It is highly recommended that you run this in a tmux shell, as it will take a long time to complete and you'll want to monitor progress by the output files. Sleeping for 5 seconds..."
	@sleep 5
	# This will run NUM_PROC SemRep instances in parallel.
	find data/raw/abstracts_split/ -name "*.txt" -type f | parallel --bar --max-procs $(NUM_PROC) $(SEMREP_BIN) -F -Z 2006 -L 2006AA -V idisk_umls {} {}.semrep_idisk_umls.out '&>' {}.semrep_idisk_umls.out.log


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
