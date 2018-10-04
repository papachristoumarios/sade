import subprocess

def cmd(_cmd):
    # Get output of command
    l = subprocess.check_output(_cmd, shell=True)
    l = [x.decode('utf-8') for x in l.splitlines()]
    l = list(filter(lambda z: z.rstrip() != '', l))
    return l

def basename(x): return x.split('/')[-1]
    
