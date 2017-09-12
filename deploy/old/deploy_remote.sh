#!/bin/bash
#@author:wyc

color_text()
{
    echo -e "\033[$2m$1\033[0m"
}

echo_normal()
{
    echo $(color_text "$1" "32")
}

echo_error()
{
    echo $(color_text "$1" "31")    
}

echo_warning()
{
    echo $(color_text "$1" "33")
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
mkdir -p $DIR/tmp
apt-get autoclean
apt-get autoremove
ver=`lsb_release -r | awk '{print $2}' | cut -d "." -f1`
if [ $ver = "14" ];then
    echo_warning "Your Ubuntu Version is low,Need More Procedure!"
	apt update
    apt-get -y install software-properties-common python-software-properties
	if [ `apt-key list | grep OpenJDK | wc -l` -eq 0 ];then
		add-apt-repository -y ppa:openjdk-r/ppa
	fi
    if [ ! -f "/etc/apt/sources.list.d/mongodb-org-3.4.list" ];then
        echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.4.list
    fi
elif [ $ver = "16" ];then
    echo_normal "Normal Install!"
	apt update
    if [ ! -f "/etc/apt/sources.list.d/mongodb-org-3.4.list" ];then
        echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
    fi
else
    echo_error "Your Linux Distribution Is Not Supported!"
    exit
fi
mongo_key_ver=`apt-key list | grep MongoDB | awk '{print $3}'`
mongo_key_num=`apt-key list | grep MongoDB | wc -l`
if [ $mongo_key_num -eq 0 -o $mongo_key_ver != "3.4" ];then
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
fi 
#Install ElasticSearch
check_install "openjdk-8-jre"
if [ $? -eq 0 ];then
    apt -y install openjdk-8-jre
fi
check_install "elasticsearch"
if [ $? -eq 0 ];then
    if [ ! -d $DIR/tmp ]; then
        mkdir -p $DIR/tmp
    fi
    if [ ! -f "$DIR/tmp/elasticsearch-5.5.1.deb" ];then
        wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.deb -P $DIR/tmp
    fi
    dpkg -i "$DIR/tmp/elasticsearch-5.5.1.deb"
fi
service elasticsearch start
es_home="/usr/share/elasticsearch"
if [ ! -d "$es_home/plugins/analysis-ik" ];then
    $es_home/bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v5.5.1/elasticsearch-analysis-ik-5.5.1.zip
fi
#Install And Config Mongodb
apt-get install -y mongodb-org
if [ ! -d "/data/db" ];then
    mkdir -p /data/db
fi
chown -R mongodb /data/db
if [ `cat /etc/rc.local | grep "#MONGODB_TAG" | wc -l` -eq 0 ]
	sed -i '#MONGODB' /etc/rc.local
	sed -i '$iif test -f /sys/kernel/mm/transparent_hugepage/enabled; then' /etc/rc.local
	sed -i '$i    echo never > /sys/kernel/mm/transparent_hugepage/enabled' /etc/rc.local
	sed -i '$ifi' /etc/rc.local
	sed -i '$iif test -f /sys/kernel/mm/transparent_hugepage/defrag; then' /etc/rc.local
	sed -i '$i    echo never > /sys/kernel/mm/transparent_hugepage/defrag' /etc/rc.local
	sed -i '$ifi' /etc/rc.local
	sed -i '$imongod --replSet bt' /etc/rc.local
fi
sudo service mongod stop
sleep 2
#if [ `ps -f -u root | grep "mongod --replSet" | wc -l` -eq 0 ];then
nohup mongod --replSet bt &
#fi
sleep 2
echo "rs.initiate()" | mongo
#config mongo-connector
apt -y install python-dev
check_install "python-pip"
if [ $? -eq 0 ];then
    apt install python-pip
fi
pip install 'mongo-connector[elastic5]'
#clean
rm -rf $DIR/tmp
apt-get autoremove
apt-get autoclean
exit
