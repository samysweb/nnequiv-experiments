#! /bin/bash

rm -rf $TMPDIR/nnequiv-repo
git clone https://github.com/samysweb/nnequiv.git $TMPDIR/nnequiv-repo
chmod -R a+rw $TMPDIR/nnequiv-repo
cd $TMPDIR/nnequiv-repo
git checkout $1 # Checkout right commit

export PYTHONPATH="$PYTHONPATH:$TMPDIR/nnequiv-repo/src"
export NNEQUIVPATH="$TMPDIR/nnequiv-repo"