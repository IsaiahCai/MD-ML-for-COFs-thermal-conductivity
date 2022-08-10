# navigate to the folder contains all cif files  
cd /Users/isaiah/Desktop/_1397batchs_/batch_1;
i=0;

for f in *

do
	
	# make a directory for each cif files and name it according to the cif file name
	mkdir "${f%.*}";
	# move files to folders accordingly
	mv $f "${f%.*}";
	
	# navigate inside each folder and Do lammps-interface conversion using Dreiding Force Fields 
	cd "${f%.*}";
	lammps-interface -ff Dreiding $f;
	cd ..;

	(( i+=1 ))
	echo "done one loop, total times is $i";
	
	# make sure each folder has <= 50 cif files
	if [ $i = 52 ];
	then 
			echo "total times is 50, stop now"
			break
	fi

done
