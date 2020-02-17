# shorewall-blacklist
ajout d'une blacklist d'ip automatiquement 

### ATTENTION

* Si une configuration Shorewall est déjà en place, vérifier que la copie de fichier ne va pas écraser la configuration existante.
* Penser, dans /etc/shorewall/shorewall.conf, à changer l'option SAVE_IPSETS de No à Yes

### NOTES 
* Pour Dedian 9 il faut installer Python 3.6
* Sous Debian 10 pas de comportement étrange constaté suite au remplacement d'iptables par nftables.
* wget a été préféré a urlretrieve (trop de changement de comportement entre deux version de urlretrieve
* la syntaxe f' a été abandonné la aussi car des changement de comportement on été constaté entre deux versions.
* Ce script a été testé en Debian 9 et 10 et est fonctionnel en l'état.
* Pensez à nourir le fichier whitelist de vos adresses IP pour ne pas etre "autoblacklisté"


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
