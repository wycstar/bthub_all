#!/bin/bash
#@author:wyc

#Function
color_text()
{
    echo "\033[$2m$1\033[0m"
}

echo_normal()
{
    echo -e $(color_text "$1" "32")
}

echo_error()
{
    echo -e $(color_text "$1" "31")    
}

echo_warning()
{
    echo -e $(color_text "$1" "33")
}

check_install()
{
    n=`sudo dpkg -s $1 | grep "install ok" | wc -l`
    if [ $n -ne 0 ];then
        return 1
    else
        return 0
    fi
}

if [ $USER != "root" ];then
    echo_error "Please Run As ROOT User!"
    exit
fi
DIR=$(cd `dirname $0`; pwd)
apt-get autoclean
apt-get autoremove
ver=`lsb_release -r | awk '{print $2}' | cut -d "." -f1`
if [ $ver = "14" ];then
    echo_warning "Your Ubuntu Version is low,Need More Procedure!"
	cp $DIR/etc/sources.list /etc/apt/sources.list
	apt update
    apt-get -y install software-properties-common python-software-properties
    if [ `apt-key list | grep OpenJDK | wc -l` -eq 0 ];then
		add-apt-repository -y ppa:openjdk-r/ppa
		apt-get update 
	fi
elif [ $ver = "16" ];then
    echo_normal "Normal Install!"
	cp $DIR/etc/sources.list /etc/apt/sources.list
	apt update
else
    echo_error "Your Linux Distribution Is Not Supported!"
    exit
fi
#Install ElasticSearch
check_install "openjdk-8-jre"
if [ $? -eq 0 ];then
    apt -y install openjdk-8-jre
fi
check_install "elasticsearch"
if [ $? -eq 0 ];then
    dpkg -i $DIR/deb/elasticsearch-5.5.1.deb
fi
if [ ! -d "/home/data/elasticsearch/log" ];then
	mkdir -p /home/data/elasticsearch/log
	chown -R elasticsearch:elasticsearch /home/data/elasticsearch/log
fi
if [ ! -d "/home/data/elasticsearch/data" ];then
	mkdir -p /home/data/elasticsearch/data
	chown -R elasticsearch:elasticsearch /home/data/elasticsearch/data
fi
service elasticsearch stop
cp $DIR/etc/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
chown root /etc/elasticsearch/elasticsearch.yml
chgrp elasticsearch /etc/elasticsearch/elasticsearch.yml
service elasticsearch start
es_home="/usr/share/elasticsearch"
if [ ! -d "$es_home/plugins/analysis-ik" ];then
    $es_home/bin/elasticsearch-plugin install file://$DIR/deb/elasticsearch-analysis-ik-5.5.1.zip
	service elasticsearch restart
fi
#config autostart
apt install -y supervisor
cp $DIR/etc/sv_mongo_connector.conf /etc/supervisor/conf.d/mongo_connector.conf
cp $DIR/etc/sv_mongod.conf /etc/supervisor/conf.d/mongod.conf
#Install And Config Mongodb
MONGO_HOME="/home/data/mongodb"
check_install "mongodb-org-server"
if [ $? -eq 0 ];then
	dpkg -i ./deb/mongodb-org-*.deb
fi
if [ ! -d "/home/data/mongodb/data" ];then
	mkdir -p $MONGO_HOME/data
fi
if [ ! -d "/home/data/mongodb/log" ];then
	mkdir -p $MONGO_HOME/log
fi
if [ ! -d "/home/data/mongodb/conf" ];then
	mkdir -p $MONGO_HOME/conf
fi
chown -R mongodb:mongodb $MONGO_HOME/data
chown -R mongodb:mongodb $MONGO_HOME/log
cp $DIR/etc/mongod.conf $MONGO_HOME/conf/mongod.conf
chown -R mongodb:mongodb $MONGO_HOME/conf/mongod.conf
if [ `cat /etc/rc.local | grep "#MONGODB_TAG" | wc -l` -eq 0 ];then
	sed -i '$i#MONGODB_TAG' /etc/rc.local
	sed -i '$iif test -f /sys/kernel/mm/transparent_hugepage/enabled; then' /etc/rc.local
	sed -i '$i    echo never > /sys/kernel/mm/transparent_hugepage/enabled' /etc/rc.local
	sed -i '$ifi' /etc/rc.local
	sed -i '$iif test -f /sys/kernel/mm/transparent_hugepage/defrag; then' /etc/rc.local
	sed -i '$i    echo never > /sys/kernel/mm/transparent_hugepage/defrag' /etc/rc.local
	sed -i '$ifi' /etc/rc.local
	sed -i '$iservice mongod stop' /etc/rc.local
	sed -i '$isleep 2' /etc/rc.local
	sed -i '$isupervisorctl start mongod' /etc/rc.local
	sed -i '$isleep 2' /etc/rc.local
	sed -i '$isupervisorctl start mongo-connector' /etc/rc.local
	sed -i '$iservice elasticsearch start' /etc/rc.local
fi
sudo service mongod stop
sleep 2
service supervisor restart
supervisorctl start mongod
sleep 2
echo "rs.initiate()" | mongo
#config mongo-connector
apt -y install python-dev
check_install "python-pip"
if [ $? -eq 0 ];then
    apt install -y python-pip
fi
pip install 'mongo-connector[elastic5]'
#install and config redis
if [ ! -d "/home/data/redis/data" ];then
	mkdir -p /home/data/redis/data
fi
if [ ! -d "/home/data/redis/log" ];then
	mkdir -p /home/data/redis/log
fi
apt install -y redis-server
chown -R redis:redis /home/data/redis/data
chown -R redis:redis /home/data/redis/log
service redis-server stop
cp $DIR/etc/redis.conf /etc/redis/redis.conf
chown root:root /etc/redis/redis.conf
if test -e $DIR/data/redis.rdb;then
	mv $DIR/data/redis.rdb /home/data/redis/data/dump.rdb
	chown redis:redis /etc/redis/redis.conf
fi
service redis-server start
sed -i '$ivm.overcommit_memory = 1' /etc/sysctl.conf
#clean
apt-get autoremove
apt-get autoclean
#config db
if test -d $DIR/data/mongodb;then
	mongorestore -d dht -c hashset $DIR/data/mongodb/*.bson
fi
curl -XPUT localhost:9200/dht
curl -XPOST localhost:9200/dht/fulltext/_mapping --data-binary @$DIR/etc/mapping.json -H "Content-type:application/json"
reboot
exit
