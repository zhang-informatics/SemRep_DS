# You probably don't want to run this directly, rather you should use the `make idisk_umls` recipe.

IDISK_DIR=$1  # iDISK version directory. E.g. iDISK/versions/1.0.1/
UMLS_VERSION=$2  # E.g. 2006AA
MTH_DIR=$3  # Directory containing UMLS Metathesaurus RRF data files.

if [ -f ${IDISK_DIR}/build/UMLS/${UMLS_VERSION}/MRCONSO.RRF ]; then
	echo "Exended UMLS version seems to already exist at ${IDISK_DIR}/build/UMLS/${UMLS_VERSION}/. Aborting."
	exit 1
fi

cd ${IDISK_DIR}/
mkdir -p build/UMLS/${UMLS_VERSION}/
python ../../lib/idlib/idlib/formatters/umls.py \
    --idisk_version_dir . \
    --umls_mth_dir ${MTH_DIR} \
    --outdir build/UMLS/${UMLS_VERSION} \
    --use_semtypes ../../lib/idlib/idlib/formatters/semantic_types_2016.txt
