# Wrapper for MoJo Distance
import subprocess
import os

os.system('javac MoJo.java')

# Wrapper for mojo distance
def mojo(source, target, mode, **args):
	cmd = 'java MoJo {} {} {} {}'.format(source, target, mode, ' '.join(args))
	out = subprocess.check_output(cmd, shell=True)
	try:
		return int(out.decode().strip())
	except:
		return None

# Generate .bunch files
def generate_bunch(partition, outfile):
	with open(outfile, 'w+') as f:
		for key, val in partition.items():
			f.write('{} = {}\n'.format(str(key), ', '.join(map(str, val))))
