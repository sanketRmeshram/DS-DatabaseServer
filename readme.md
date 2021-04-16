## Accessing web servers
* webserver - http://13.59.136.130:5000/
* bacup_webserver - http://18.219.37.235:5000/


## Fault tolerant messages
`node 'x' with 'ip' just died`

## setup git on server via ssh
```
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add /home/ubuntu/.ssh/id_ed25519

# copy key to clipboard
cat /home/ubuntu/.ssh/id_ed25519.pub
```
paste this to https://github.com/settings/keys


## Instructions for webserver
```
sudo apt update
sudo apt install python3-pip
sudo apt-get python3-venv
python3 -m venv webserver
source webserver/bin/activate
cd ds_webserver
pip3 install -r requirements.txt

```


## Instructions for Database servers
```
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql
 >CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
 >GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' WITH GRANT OPTION;
 >FLUSH PRIVILEGES;
 >CREATE SCHEMA DSTRY; (To make one)
 >exit

mysql -u user -p
 >password
 >CREATE SCHEMA DSTRY; (To make one)
 >DROP SCHEMA DSTRY; (To delete one)

sudo apt install python3-pip
pip3 install -r requirements.txt
```
