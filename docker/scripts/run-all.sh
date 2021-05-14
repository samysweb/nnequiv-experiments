#! /bin/bash
source variables.sh
mkdir -p $TMPDIR

machine_info(){
	{
		echo "******* Variables *******"
		cat $EXPERIMENT_DIR/variables.sh
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
		cd $EXPERIMENT_DIR
		echo "******* Experiment Repository *******"
		git --no-pager show --pretty=short --shortstat
		git --no-pager status
		echo "******* nnequiv Repository *******"
		cd $NNEQUIVPATH
		git --no-pager show --pretty=short --shortstat
		git --no-pager status
	} > "$1" 2>&1
}

# run_nnequiv resultDirOverall inputFile1 inputFile2 property epsilon
run_nnequiv(){
	cd $EXPERIMENT_DIR
	# Check if files exist
	nnequiv_input1="$2.onnx"
	nnequiv_input2="$3.onnx"
	if [ ! -f "$nnequiv_input1" ]; then
		echo "File $nnequiv_input1 not found!"
		exit
	fi
	if [ ! -f "$nnequiv_input2" ]; then
		echo "File $nnequiv_input2 not found!"
		exit
	fi

	# Check if ran before else create directory
	nnequiv_resultDir="$1/nnequiv-$NNEQUIV_COMMIT/"
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
		cd $nnequiv_outDir
		runlim -r $TO -s $MO python $NNEQUIVPATH/examples/equiv/test.py $nnequiv_input1 $nnequiv_input2 $4 $5
	} > $nnequiv_outDir/stdout.log 2> $nnequiv_outDir/stderr.log
	cp $nnequiv_outDir/* "$nnequiv_resultDir"
	chmod -R a+rwx "$nnequiv_resultDir"
}

exec_bench(){
	cd $EXPERIMENT_DIR

	inputFile1=`pwd`/benchmarks/$1
	inputFile2=`pwd`/benchmarks/$1-mirror
	
	resultDirOverall=`pwd`"/results/$1-$2-$3/"
	mkdir -p $resultDirOverall

	for ((num=1;num<=RUN_COUNT;num++)); do
		echo "Run $num"
		run_nnequiv "$resultDirOverall/$num" $inputFile1 $inputFile2 $2 $3
	done
	chmod -R a+rwx $resultDirOverall
}


IFS=","
echo "Preparing NNEquiv..."
source $EXPERIMENT_DIR/nnequiv/setup.sh $NNEQUIV_COMMIT
cd $EXPERIMENT_DIR
echo "Reading benchmark instances from $1"
while read bench arg1 arg2; do
	echo $bench
	exec_bench $bench $arg1 $arg2
done < $INSTANCES