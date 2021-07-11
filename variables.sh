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
	TMPDIR=/raid/steuber/tmp2
fi
INSTANCES=instances-tightness.csv
INSTANCES_BUENING=instances-tightness-buening.csv

# How often are benchmarks run?
RUN_COUNT=1

# NNEquiv Commit
NNEQUIV_COMMIT="7417a86"
BUENING_COMMIT="04f3bfb" # speedup branch (modified for ONNX Parsing)

TO=10800
MO=2048
