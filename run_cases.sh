#!/bin/bash

# define simulation cases

simulatorExe="./sim"

declare -a num_nodes_cases=(100 1000 2000 5000 10000 )
declare -a percentage_malicious=( 5 20 22 ) #(0  5  10  15  20  22 23 25 30)

outputfile="./cases_output.csv"

#########################################
### EXECUTION START
########################################

## TRAP signals for script stopping
trap 'excode=$?; echo signal received $excode ; trap - EXIT; kill -s 9 $jobs -p); wait' INT TERM

########################################



STARTM=`date -u "+%s"`


echo "Running all cases"

for nncase in "${num_nodes_cases[@]}"; do
	for pcmal in "${percentage_malicious[@]}";do
		echo --num_nodes $nncase --num_malicious $( echo $pcmal $nncase | awk '{printf "%d\n",$1*$2/100}')
		$simulatorExe --num_nodes $nncase --num_malicious $( echo $pcmal $nncase | awk '{printf "%d\n",$1*$2/100}') >> $outputfile 
	done
done

STOPM=`date -u "+%s"`
RUNTIMEM=`expr $STOPM - $STARTM`

if (($RUNTIMEM>59)); then
	TTIMEM=`printf "%d days %dh%dm%ds\n" $((RUNTIMEM/86400%365)) $((RUNTIMEM/3600%24)) $((RUNTIMEM/60%60)) $((RUNTIMEM%60))`
else
	TTIMEM=`printf "%ds\n" $((RUNTIMEM))`
fi

echo "Total execution time of simulation : $TTIMEM"

echo "Bye Bye!"
exit;


