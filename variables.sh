#! /bin/bash
# Directories & Index of Instances
EXPERIMENT_DIR=`pwd`
EXPERIMENT_DIR_BUENING=`pwd`
# ATTENTION: We run rm -rf on TMPDIR!
TMPDIR=~/THISNONEXISTANTPATH
if [[ "$(hostname)" = "hal9000" ]]; then
	TMPDIR=/tmp/steuber/experiment
fi
if [[ "$(hostname)" = "baldur3" ]]; then
	TMPDIR=/raid/steuber/tmp3
fi
INSTANCES=instances-counterexamples.csv
INSTANCES_BUENING=instances-counterexamples-buening.csv

# How often are benchmarks run?
RUN_COUNT=3

# NNEquiv Commit
NNEQUIV_COMMIT="06a2d52"
BUENING_COMMIT="04f3bfb" # speedup branch (modified for ONNX Parsing)

TO=120
MO=512
