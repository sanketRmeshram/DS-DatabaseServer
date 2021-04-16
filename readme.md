# setup git on server via ssh
```
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# copy key to clipboard
sudo apt-get install xclip
xclip -selection clipboard < ~/.ssh/id_ed25519.pub
```
paste this to https://github.com/settings/keys



# Instructions
- sudo apt update
- sudo apt install mysql-server
- sudo mysql_secure_installation
- sudo mysql
- CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
- GRANT ALL PRIVILEGES ON \*.\* TO 'user'@'localhost' WITH GRANT OPTION;
- FLUSH PRIVILEGES;
- exit
- mysql -u user -p
- password
- CREATE SCHEMA DSTRY; (To make one)
- DROP SCHEMA DSTRY; (To delete one)
- sudo apt install python3-pip
- pip3 install -r requirements.txt
