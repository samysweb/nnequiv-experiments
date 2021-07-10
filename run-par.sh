#! /bin/bash
source variables.sh
mkdir -p $TMPDIR

machine_info(){
	source $2
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

# run_nnequiv resultDirOverall inputFile1 inputFile2 property epsilon strategy varpath
run_nnequiv(){
	source $7
	VAR_PATH=`pwd`/variables.sh
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
	echo "Results will be stored in $nnequiv_resultDir"

	# Write out machine info and initialize nnequiv with right commit
	machine_info "$nnequiv_resultDir/init.log" $VAR_PATH
	{
		cd $nnequiv_resultDir
		export OMP_NUM_THREADS=1
		runlim -r $TO -s $MO python $NNEQUIVPATH/examples/equiv/test.py $nnequiv_input1 $nnequiv_input2 $4 $5 $6
	} > $nnequiv_resultDir/stdout.log 2> $nnequiv_resultDir/stderr.log
	chmod -R a+rwx "$nnequiv_resultDir"
}

exec_bench(){
	source variables.sh
	VAR_PATH=`pwd`/variables.sh
	IFS=","
	read -r bench input property strategy <<< "$1"
	echo "Running $bench..."
	if [[ "$strategy" = "CEGAR_OPTIMAL" ]]; then
		TO_OLD=$TO
		TO=15000
	fi
	cd $EXPERIMENT_DIR

	inputFile1=`pwd`/benchmarks-versions/$bench
	inputFile2=`pwd`/benchmarks-versions/$bench-mirror
	
	resultDirOverall=`pwd`"/results/$bench-$input-$property-$strategy/"
	mkdir -p $resultDirOverall
	echo "Prepared directory $resultDirOverall, now executing runs..."
	for ((num=1;num<=RUN_COUNT;num++)); do
		echo "Running $num"
		run_nnequiv "$resultDirOverall/$num" $inputFile1 $inputFile2 $input $property $strategy $VAR_PATH
	done
	chmod -R a+rwx $resultDirOverall
	echo "Done with runs"
	if [[ "$strategy" = "CEGAR_OPTIMAL" ]]; then
		TO=$TO_OLD
	fi
}

source $EXPERIMENT_DIR/nnequiv/setup.sh $NNEQUIV_COMMIT
cd $EXPERIMENT_DIR

export -f machine_info
export -f run_nnequiv
export -f exec_bench

parallel -j 4 exec_bench :::: $INSTANCES