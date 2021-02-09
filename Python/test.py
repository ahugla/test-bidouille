

import paramiko     # pip3 install paramiko
import time         # pas besoin de metttre en dependance car deja dans librairie par defaut

#-----------------------------
# Variables
counter_sleep = 2 # counter sleep duration in while loop


#-----------------------------

def executeSSHcommand(server, login, password, command):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())    # pas de check de clé
  client.connect(server, username=login, password=password)
  ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
  # affichage de la sortie de la commande
  for line in ssh_stdout:
    print('... ' + line.strip('\n'))
  client.close()
  local_retour = "OK"
  return local_retour

#-----------------------------

#def wait_for_master():
#  time.sleep(5)  

#----------------------------- 
 
salt_master = "vrasaltstack.cpod-vrealize.az-fkd.cloud-garage.net"
username="root"
salt_master_password = "VMware1!"
minion="vra-001111"
#logs
print("server salt master : " +salt_master)


wait_for_master()
print("fin du sleep")



#On attent que le minion soit en etat "unregistered" ou que le counter soit a 10 tentatives
retour = "0"
counter = 0
while (retour == "0") and (counter < 10):
  # Creation de la commande
  cmd_to_execute="salt-key --list=pre | grep " +minion +" | wc -l"
  print("command to execute : " +cmd_to_execute)
  # execution SSH
  #retour=executeSSHcommand(salt_master,username,salt_master_password,cmd_to_execute)
  print("retour: " +retour)
  time.sleep(counter_sleep) 
  counter = counter + 1
  print("counter: " +str(counter))





 




