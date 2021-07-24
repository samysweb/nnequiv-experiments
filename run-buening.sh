#! /bin/bash
source variables.sh
mkdir -p $TMPDIR

machine_info(){
	source $EXPERIMENT_DIR_BUENING/variables.sh
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
	source $EXPERIMENT_DIR_BUENING/variables.sh
	echo $EXPERIMENT_DIR_BUENING
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
	nnequiv_resultDir="$1/buening-$BUENING_COMMIT/"
	if [ -d "$nnequiv_resultDir" ]; then
		echo "Result directory already exists, skipping"
		return;
	fi
	mkdir -p "$nnequiv_resultDir"

	# Write out machine info and initialize nnequiv with right commit
	machine_info "$nnequiv_resultDir/init.log"
	
	{
		cd $EXPERIMENT_DIR_BUENING
		PYTHONPATH="$PYTHONPATH:`pwd`/nnequiv-repo/examples/equiv/:`pwd`/NNEquivalence-repo" runlim -r $TO -s $MO python run_buening.py $nnequiv_input1 $nnequiv_input2 $4 $5 $6
	} > $nnequiv_resultDir/stdout.log 2> $nnequiv_resultDir/stderr.log
	
	chmod -R a+rwx "$nnequiv_resultDir"
}

exec_bench(){
	cd $EXPERIMENT_DIR_BUENING

	source variables.sh
	VAR_PATH=`pwd`/variables.sh
	IFS=","
	read -r bench input property strategy <<< "$1"
	
	inputFile1=`pwd`/benchmarks-versions/$bench
	inputFile2=`pwd`/benchmarks-versions/$bench-mirror
	
	resultDirOverall=`pwd`"/results-counter/$bench-$input-$property-$strategy/"
	mkdir -p $resultDirOverall

	for ((num=1;num<=RUN_COUNT;num++)); do
		echo "Run $num"
		run_buening "$resultDirOverall/$num" $inputFile1 $inputFile2 $input $property $strategy
	done
	chmod -R a+rwx $resultDirOverall
}


git clone https://github.com/samysweb/NNEquivalence NNEquivalence-repo
cd ./NNEquivalence-repo
git checkout $BUENING_COMMIT
cd ../
git clone https://github.com/samysweb/nnequiv.git nnequiv-repo
cd ./nnequiv-repo
git checkout $NNEQUIV_COMMIT
cd ../

cd $EXPERIMENT_DIR_BUENING

export EXPERIMENT_DIR_BUENING
export -f machine_info
export -f run_buening
export -f exec_bench

parallel -j 8 exec_bench :::: $INSTANCES_BUENING
#op and noop!

rm -rf NNEquivalence-repo
rm -rf nnequiv-repo