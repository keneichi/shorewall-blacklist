# shorewall-blacklist
ajout d'une blacklist d'ip automatiquement 

### ATTENTION

* Si une configuration Shorewall est déjà en place, vérifier que la copie de fichier ne va pas écraser la configuration existante.
* Pour le formatage de ce type : bl_tmp = f'{work_path}/bl_tmp' il est impératif d'être en python 3.6 au minimum.
### NOTES 
* Ce script a été testé en Debian 9 et 10. 
* Pour Dedian 9 il faut installer Python 3.6
* Sous Debian 10 pas de comportement étrange constaté suite au remplacement d'iptables par nftables.



### Installer les dépendances nécessaires

apt install python3-pip ipset ipset-persistent

pip3 install wget

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
