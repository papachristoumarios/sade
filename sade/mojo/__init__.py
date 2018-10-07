# Wrapper for MoJo Distance 
import subprocess 
import os

os.system('javac MoJo.java') 

def mojo(source, target, mode, **args):
	out = subprocess.check_output('java MoJo {} {} {}'.format(source, target, ' '.join(args)), shell=True)
	return out
