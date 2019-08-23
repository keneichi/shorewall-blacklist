#!/usr/bin/python3

import os
import re
import sys
import shutil
from urllib.request import urlretrieve
import ipaddress
import logging


# logfile
logging.basicConfig(filename='/var/log/shorewall-blacklist.log', filemode='w+',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

CODE_ERROR = 1
# command lines
shorewall_check = 'shorewall check'
shorewall_restart = 'shorewall restart'

# Vérification du shorewall avant les opérations
logging.info("Vérification de la configuration actuelle de shorewall.")

result = os.system(shorewall_check)
if result == 0:
    logging.info(
        "La configuration initiale de shorewall semble être correcte.")
else:
    logging.critical(
        "La configuration initiale de shorewall n'est pas valide. Le processus est arrêté. Veuillez vérifier votre configuration shorewall avant de poursuivre.")
    sys.exit(CODE_ERROR)

# Test de la présence de la base ipset
# command lines
create_blacklist_base = 'ipset create blacklist hash:ip hashsize 16777216 maxelem 16777216'

# commands
result_test_ipset = os.system('ipset add blacklist 8.8.8.8')
if result_test_ipset == 0:
    logging.info("La base existe.")
    os.system("ipset del blacklist 8.8.8.8")
else:
    logging.info(
        "la base ipset est inexistante. Création de la base ipsset blacklist")
    os.system(create_blacklist_base)
    logging.info("La base ipset a été créée.")


# sauvegarde de la configuration existante
# command lines & paths
ipsetconf = '/etc/ipset.conf'
backup_ipsetconf = '/etc/ipset.conf.backup'

# commands
logging.info("Sauvegarde de la blacklist actuelle.")
if os.path.isfile(ipsetconf):
    shutil.copy(ipsetconf, backup_ipsetconf)
    logging.info(
        "L'ancienne configuration a correctement été sauvegardée.")
else:
    logging.info("Aucune configuration à sauvegarder.")
    pass

# recupération de la liste des ip via projet stamparm/ipsum
# paths
url_ipsum = 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt'
ipsum_path = '/opt/shorewall-blacklist/'
# commands
logging.info("Recupération des adresses IP BlackListée sur projet ipsum.")
urlretrieve(url_ipsum, ipsum_path)

# creation du fichier blacklist depuis ipsum.txt
# command lines et path
logging.info("Création du fichier blacklist.")
ipsum = f'{ipsum_path}/ipsum.txt'
ipfile_blacklist = open(f'{ipsum_path}/blacklistip', 'w')
new_list = []

# commands
with open(ipsum) as ipsum:
    for line in ipsum:
        if '#' in line:
            continue
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
        try:
            ipaddress.ip_address(ip[0])
        except ValueError:
            logging.warning(
                f"L'adresse IP {ip[0]} n'est pas valide et n'a pas été ajouté à la blacklist.")
            continue
        ipfile_blacklist.write(ip[0]+'\n')
        new_list.append(ip[0])

ipfile_blacklist.close()

# préparation pour diff
# commands and path
bl_tmp = f'{ipsum_path}/bl_tmp'
rm_bltmp = f'rm -f {ipsum_path}/bl_tmp'
create_bltmp = f'ipset list blacklist > {ipsum_path}/bl_tmp'
old_list = []

# commands
os.system(create_bltmp)

with open(bl_tmp) as f:
    for line in f.readlines():
        try:
            ipaddress.ip_address(line.strip())
        except ValueError:
            continue
        old_list.append(line.strip())

os.system(rm_bltmp)

# obtenir les anciennes IP blacklistées
del_list = list(set(old_list) - set(new_list))

# obtenir les adresses nouvellement blacklisées
add_list = list(set(new_list) - set(old_list))

# création de la liste d'adresse à ajouter
f_add = open(f'{ipsum_path}/add_list.txt', 'w')
f_add.writelines('\n'.join(add_list))
f_add.close()

# création de la liste d'adresse à supprimer
f_del = open(f'{ipsum_path}/del_list.txt', 'w')
f_del.writelines('\n'.join(del_list))
f_del.close()


# injection data dans base
# command lines et path
addipset = 'ipset add blacklist '
delipset = 'ipset del blacklist '
del_list = f'{ipsum_path}/del_list.txt'
add_list = f'{ipsum_path}/add_list.txt'
blacklist = f'{ipsum_path}/blacklistip'
ipsum_file = f'{ipsum_path}/ipsum.txt'

# commands
logging.info("Injection des regles ipset dans la base")
if os.path.isfile(ipsetconf):
    with open(del_list) as dellist:
        for line in dellist:
            os.system(f"{delipset} {line}")
            logging.info(
                f"L'adrese IP suivante a été supprimée de la blacklist existante : {line.strip()}")

    with open(add_list) as addlist:
        for line in addlist:
            os.system(f"{addipset} {line}")
            logging.info(
                f"L'adrese IP suivante a été ajoutée à la blacklist existante : {line.strip()}")
else:
    with open(blacklist) as blacklist:
        for line in blacklist:
            os.system(f"{addipset} {line}")
            logging.info(
                f"L'adrese IP suivante a été correctement ajoutée à la blacklist : {line.strip()}")

# nettoyage après opérations
logging.info("Suppression des fichiers de travail")
list_files = [blacklist, ipsum_file, add_list, del_list]

for files in list_files:
    os.remove(files)
    logging.info(f'Le fichier de travail "{files}" a été supprimé')


# sauvegarde des regles actuelles ipset
# command lines
ipset_save = 'ipset save > /etc/ipset.conf'

# commands
logging.info("Sauvegarde des regles ipset blacklist.")
os.system(ipset_save)

# redemarrage de shorewall
# path et command lines
blrules_file = '/etc/shorewall/blrules'
# commands
logging.info("copie du fichier blrules")
if not os.path.isfile(blrules_file):
    os.system(
        f'cp {ipsum_path}/configfiles/blrules /etc/shorewall/blrules')


logging.info("Vérification de la configuration shorewall.")
result = os.system(shorewall_check)

if result == 0:
    os.system(shorewall_restart)
    logging.info("Shorewall a été correctement redémarré.")
else:
    logging.critical("Une erreur est survenue. Arret du processus.")
    sys.exit(CODE_ERROR)
