

import paramiko     # pip3 install paramiko
import time         # pas besoin de metttre en dependance car deja dans librairie par defaut

#-----------------------------Variables

counter_sleep = 2 # duree entre chaque tentative
counter_max = 10 # nombre de tentavives max
#salt_master = "vrasaltstack.cpod-vrealize.az-fkd.cloud-garage.net"
salt_master = "10.11.10.29"
username="root"
#salt_master_password = "VMware1!"
salt_master_password = "changeme"

#TEMP
minion="vra-001517"

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
  local_retour = 1
  return local_retour

#-----------------------------
#logs
print("server salt master : " +salt_master)



#On attent que le minion soit en etat "unregistered" ou que le counter soit a 10 tentatives
retour = 1
counter = 0
while (retour == 1) and (counter < counter_max):
  # Creation de la commande
  cmd_to_execute="salt-key --list=pre | grep " +minion +" | wc -l"
  print("command to execute : " +cmd_to_execute)
  # execution SSH
  retour=executeSSHcommand(salt_master,username,salt_master_password,cmd_to_execute)
  time.sleep(counter_sleep) 
  counter = counter + 1
  print("retour: " +retour)
  print("counter: " +str(counter))





 





