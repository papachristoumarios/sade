# Wrapper for MoJo Distance 
import subprocess 
import os

os.system('javac MoJo.java') 

# Wrapper for mojo distance
def mojo(source, target, mode, **args):
	out = subprocess.check_output('java MoJo {} {} {}'.format(source, target, ' '.join(args)), shell=True)
	try:
		return int(out.decode().strip())
	except:
		return None

# Generate .bunch files
def generate_bunch(partition, outfile):
	with open(outfile, 'w+') as f:
		for key, val in partition.items():
			f.write('SS({}.ss) = {}'.format(val[0], ', '.join(val))

		