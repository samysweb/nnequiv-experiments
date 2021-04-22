#! /bin/bash

rm -rf /tmp/nnequiv-repo
git clone git@github.com:samysweb/nnequiv.git /tmp/nnequiv-repo
chmod -R a+rw /tmp/nnequiv-repo
cd /tmp/nnequiv-repo
git checkout $1 # Checkout right commit

export PYTHONPATH="$PYTHONPATH:/tmp/nnequiv-repo/src"
export NNEQUIVPATH="/tmp/nnequiv-repo"