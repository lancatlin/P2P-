import  paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

key = paramiko.RSAKey.from_private_key(open('id_rsa'))
ssh.connect(hostname='github.com/lancatlin/P2P-',username='lancatlin',pkey=key,timeout=10)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('uptime')
print(ssh_stdout.read())
ssh.close()