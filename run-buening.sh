#! /bin/bash
source variables.sh
mkdir -p $TMPDIR

machine_info(){
	{
		echo "******* Variables *******"
		cat $EXPERIMENT_DIR_BUENING/variables.sh
		echo "******* Machine details *******"
		echo "$ hostname"
		hostname
		echo "$ lscpu"
		lscpu
		echo "$ cat /proc/meminfo"
		cat /proc/meminfo
		echo "$ cat /proc/version"
		cat /proc/version
		echo "$ lsblk"
		lsblk
		cd $EXPERIMENT_DIR_BUENING
		echo "******* Experiment Repository *******"
		git --no-pager show --pretty=short --shortstat
		git --no-pager status
		echo "******* NN Equivalence Repository *******"
		cd $EXPERIMENT_DIR_BUENING/NNEquivalence-repo
		git --no-pager show --pretty=short --shortstat
		git --no-pager status
		echo "******* nnequiv Repository *******"
		cd $EXPERIMENT_DIR_BUENING/nnequiv-repo
		git --no-pager show --pretty=short --shortstat
		git --no-pager status
	} > "$1" 2>&1
}

# run_buening resultDirOverall inputFile1 inputFile2 property epsilon noop?
run_buening(){
	cd $EXPERIMENT_DIR_BUENING
	echo $EXPERIMENT_DIR_BUENING
	# Check if files exist
	nnequiv_input1="$2.h5"
	nnequiv_input2="$3.h5"
	if [ ! -f "$nnequiv_input1" ]; then
		echo "File $nnequiv_input1 not found!"
		exit
	fi
	if [ ! -f "$nnequiv_input2" ]; then
		echo "File $nnequiv_input2 not found!"
		exit
	fi

	# Check if ran before else create directory
	nnequiv_resultDir="$1/buening-$BUENING_COMMIT/"
	if [ -d "$nnequiv_resultDir" ]; then
		echo "Result directory already exists, skipping"
		return;
	fi
	mkdir -p "$nnequiv_resultDir"
	rm -rf "$TMPDIR/*"
	nnequiv_outDir=$TMPDIR

	# Write out machine info and initialize nnequiv with right commit
	machine_info "$nnequiv_outDir/init.log"
	
	{
		cd $EXPERIMENT_DIR_BUENING
		PYTHONPATH="$PYTHONPATH:`pwd`/nnequiv-repo/examples/equiv/:`pwd`/NNEquivalence-repo" runlim -r $TO -s $MO python run_buening.py $nnequiv_input1 $nnequiv_input2 $4 $5 $6
	} > $nnequiv_outDir/stdout.log 2> $nnequiv_outDir/stderr.log
	cp $nnequiv_outDir/* "$nnequiv_resultDir"
	chmod -R a+rwx "$nnequiv_resultDir"
}

exec_bench(){
	cd $EXPERIMENT_DIR_BUENING

	inputFile1=`pwd`/benchmarks/$1
	inputFile2=`pwd`/benchmarks/$1-mirror
	
	resultDirOverall=`pwd`"/results/$1-$2-$3-$4/"
	mkdir -p $resultDirOverall

	for ((num=1;num<=RUN_COUNT;num++)); do
		echo "Run $num"
		run_buening "$resultDirOverall/$num" $inputFile1 $inputFile2 $2 $3 $4
	done
	chmod -R a+rwx $resultDirOverall
}


IFS=","
git clone https://github.com/phK3/NNEquivalence.git NNEquivalence-repo
cd ./NNEquivalence-repo
git checkout $BUENING_COMMIT
cd ../
git clone https://github.com/samysweb/nnequiv.git nnequiv-repo
cd ./nnequiv-repo
git checkout $NNEQUIV_COMMIT
cd ../
echo "Reading benchmark instances from $1"
while read bench arg1 arg2; do
	echo $bench
	echo "Normal"
	exec_bench $bench $arg1 $arg2 ""
	echo "No Bound Optimization"
	exec_bench $bench $arg1 $arg2 "noop"
done < $INSTANCES_BUENING

rm -rf NNEquivalence-repo
rm -rf nnequiv-repo