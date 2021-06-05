# Directories & Index of Instances
EXPERIMENT_DIR=/benchmarking
EXPERIMENT_DIR_BUENING=`pwd`
# ATTENTION: We run rm -rf on TMPDIR!
TMPDIR=/tmp/experiment
INSTANCES=instances.csv
INSTANCES_BUENING=instances-buening.csv

# How often are benchmarks run?
RUN_COUNT=1

# NNEquiv Commit
NNEQUIV_COMMIT="48e7b4a"
BUENING_COMMIT="a5c91be"

TO=32400 # 9h per instance due to intense computations...
MO=4096
