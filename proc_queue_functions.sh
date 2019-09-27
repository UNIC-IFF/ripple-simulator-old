#!/bin/bash
########################################################################
##############  PROCESSES QUEUE MANAGEMENT FUNCTIONS  ##################
########################################################################

QLEN=0
PROC_QUEUE=""
MAX_NPROC=4

function proc_enqueue {
	PROC_QUEUE="$PROC_QUEUE $1"
	QLEN=$(($QLEN+1))
	#echo "$1 enqueued"
}

function proc_regeneratequeue {
	local __OLDREQUEUE=$PROC_QUEUE
    PROC_QUEUE=""
    QLEN=0
    for PID in $__OLDREQUEUE
    do
        if [ -d /proc/$PID  ] ; then
            PROC_QUEUE="$PROC_QUEUE $PID"
            QLEN=$(($QLEN+1))
        fi
    done
}


function proc_checkqueue {
    local __OLDCHQUEUE=$PROC_QUEUE
    for PID in $__OLDCHQUEUE
    do
        if [ ! -d /proc/$PID ] ; then
            proc_regeneratequeue # at least one PID has finished
           # echo "$PID  dequeued"
            break
        fi
    done
}
