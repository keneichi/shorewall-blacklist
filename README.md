# shorewall-blacklist
ajout d'une blacklist d'ip automatiquement 

## ATTENTION

* Si une configuration Shorewall est déjà en place, vérifier que la copie de fichier ne va pas écraser la configuration existante.
* Ce script n'a pas été testé en Debian 10 Buster en raison du remplacement de iptables par nftables
* Pour le formatage de ce type : bl_tmp = f'{work_path}/bl_tmp' il est impératif d'être en python 3.6 au minimum.


### Installer les dépendances nécessaires

apt install python3-pip ipset


### Créer le repertoire pour les scripts

mkdir /etc/shorewall/scripts/


### récupérer le script

cd /opt

git clone  https://github.com/keneichi/shorewall-blacklist.git


### Copier les scripts shorewall

cp /opt/shorewall-blacklist/configfiles/started /etc/shorewall/started

cp /opt/shorewall-blacklist/configfiles/ipset.sh /etc/shorewall/scripts/ipset.sh

chmod +x /etc/shorewall/scripts/ipset.sh


### Crontab

cp /opt/shorewall-blacklist/configfiles/shorewall-blacklist /etc/cron.d/shorewall-blacklist

/etc/init.d/cron restart


### Lancer le script

python3 /opt/shorewall-blacklist/blacklist.py
