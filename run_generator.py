import os

stream = os.popen('/home/dgit/dgit_env/bin/python /home/dgit/d-git-server/generate_ssh_token.py')
output = stream.read()
print(output.strip())