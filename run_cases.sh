#!/bin/bash

# define simulation cases

simulatorExe="./sim"

declare -a num_nodes_cases=(50 100 200 400 800 1000 ) #  1200 1500 2000
#declare -a percentage_malicious=( 0 1 2 4 5 8 10 15 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 55 60 70 80 85) #(0 1 2 4  5 8 10  15  20  22 23 25 30)
declare -a percentage_malicious=( 0 5 10 15 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 40 45 50 ) #(0 1 2 4  5 8 10  15  20  22 23 25 30 70 80 85)
declare -a overlappingUNLs=(0.9 0.91 0.95 0.99)

outputfile="./cases_output2.csv"

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
		for ovUNLs in "${overlappingUNLs[@]}"; do
			echo --num_nodes $nncase --mal_nodes_pC $pcmal --overlappingUNLs $ovUNLs
			# $simulatorExe --num_nodes $nncase --num_malicious $( echo $pcmal $nncase | awk '{printf "%d\n",$1*$2/100}') >> $outputfile 
			$simulatorExe --num_nodes $nncase --mal_nodes_pC $pcmal  --overlappingUNLs $ovUNLs >> $outputfile 
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


