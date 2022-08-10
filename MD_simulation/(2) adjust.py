import os,sys
import glob  
import shutil

 
path = "$path to the folder you place all folders containing cifs"
os.chdir(path)

def write_HPC_submission_script(cof):
	with open('$the path to the submission sript template (for high-performance computer)', 'r') as rf:

		with open(cof + '/submission_script','w') as wf:
			for line in rf:
				wf.write(line) 
			wf.close()
			print('writing done')

		# change variables in the submission file
		with open(cof + '/submission_script','r') as wf:
			list_of_lines = wf.readlines()
			cof_list = cof.split("/")
			cof_name = cof_list[-1]
			list_of_lines[0] = '#PBS -N '+ cof_name + '\n'
			list_of_lines[19] ='lmp -in in.'+ cof_name + '\n'
			wf.close()

		with open(cof + '/submission_script','w') as wf:
			wf.writelines(list_of_lines)
			wf.close()
	rf.close()



def modify_lammps_input_script(cof):
	template = open('$the path to LAMMPS "in." template', 'r')
	list_of_lines = template.readlines()
	template.close()
	print(len(list_of_lines))
	cof_list = cof.split("/")
	cof_name = cof_list[-1]
	input_script = open(cof + '/in.'+cof_name, 'a')
	input_script.writelines(list_of_lines)
	input_script.close()


for batch in glob.glob(path+'/*'):
	for cof in glob.glob(batch+'/*'):
		print(cof) 
		write_HPC_submission_script(cof)
		modify_lammps_input_script(cof)
