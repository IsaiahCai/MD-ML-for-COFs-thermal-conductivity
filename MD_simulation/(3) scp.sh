# 
for batch in '$path to the folders (containing cifs files)'/*
do
    expect expect.exp $batch '$destination path on high-performance computer' login.hpc.imperial.ac.uk '$account' '$password'
done
