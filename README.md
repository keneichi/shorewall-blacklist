# shorewall-blacklist
ajout d'une blacklist d'ip automatiquement 

===ATTENTION===

* Si une configuration Shorewall est déjà en place, vérifier que la copie de fichier ne va pas écraser la configuration existante.
* Ce script n'a pas été testé en Debian 10 Buster en raison du remplacement de iptables par nftables

===Installer les dépendances nécessaires===

apt install python3-pip ipset
pip3 install wget

===Créer le repertoire pour les scripts===

mkdir /etcshorewall/scripts/

===Copier les scripts shorewall===

cp /opt/shorewall-blacklist/configfiles/started /etc/shorewall/started
cp /opt/shorewall-blacklist/configfiles/ipset.sh /etc/shorewall/scripts/ipset.sh
chmod +x /etc/shorewall/scripts/ipset.sh

===Crontab===

cp /opt/shorewall-blacklist/configfiles/shorewall-blacklist /etc/cron.d/shorewall-blacklist
/etc/init.d/cron restart

===Lancer le script===

python3 /opt/shorewall-blacklist/blacklist.py
