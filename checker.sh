while true;
do
    N=$(qstat | wc -l)
    sub_N=$(( 50 - $N ))
    i=0
    # Note: qstat | wc -l should be 52 when job number is 50. But it is a bit tricky to deal with. So just do $N -lt 50 for simplicity. 
    if [[ $N -lt 50 && $i -lt $sub_N ]]
    then
        cd /rds/general/user/ic21/home/batch/new_to_qsub_in_work
        for batch in *
        do
            cd /rds/general/user/ic21/home/batch/new_to_qsub_in_work/$batch
            for dir in *
            do
                # if the file "log.submission" does't exist and submitted job is less than needed
                if [[ ! -f /rds/general/user/ic21/home/batch/new_to_qsub_in_work/$batch/$dir/log.submission && $i -lt $sub_N ]]
                then
                    # We generate a text file named "log.submission" after qsub in order to help us identify the folders that have been modified 
                    cd $dir && qsub general-mpi | tee /rds/general/user/ic21/home/batch/new_to_qsub_in_work/$batch/$dir/log.submission && cd ..
                    (( i+=1 )) && echo 'total submission is '$i', now in '$batch' and '$dir |  tee -a /rds/general/user/ic21/home/batch/log/$batch.log
                fi
            done
        done
    fi
    echo "regular check: N is now $N"
    date +"%H:%M:%S"
    echo "---------------------------"
    sleep 300
done


# Explanation

# The example architecture: 
# batch 
#   - new_to_qsub_in_work 
#       - batch_1 | batch_2 | batch_3 | ...             (This is the first for loop)
#           - structure1, structure2, ... (in batch_1) | structure_a, structure_b, ... (in batch_2) | ...            (This is the second for loop)

# The main idea: check if there is any calculation done every 5 minutes. If so, automatically submit. In addition, make sure we submit the one that has not been calculated by "Marking" the folder.  