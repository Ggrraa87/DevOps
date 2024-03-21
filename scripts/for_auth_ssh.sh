sudo apt install curl
curl -V
ip=$(curl -s ifconfig.co)
file="$hostname-$ip"
git config --global user.name "Ggrraa87"
git config --global user.email "vip.tab2002@gmail.com"

sudo apt-get update -y
sudo apt-get install -y openssh-server
sudo apt install git
sudo ufw allow 22

echo "Enter admin ssh .pub key:"
read key

# Setting up Git
mkdir MonitoringDocker
git init ~/MonitoringDocker
mkdir ~/.ssh


# Creating and setting up SSH keys

touch ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 644 ~/.ssh/authorized_keys

ssh-keygen -t rsa  -f ~/.ssh/$file -N ''

# Adding admin's public key to authorized_keys
echo "$key" | tee -a ~/.ssh/authorized_keys

# Copying the key to the remote server
ssh-copy-id -i ~/.ssh/"$file.pub" ubuntu@13.50.4.224 
	
# Work with Git
cp "/home/ubuntu/.ssh$file.pub" ~/MonitoringDocker
cd ~/MonitoringDocker
if (git status | grep "$file.pub"); then
    git checkout -b "$file" #branch 
    git add "$file.pub"
    git commit -m "$file SSH-key for $file"
    
    # Checking if the remote repository exists
    if ! git remote | grep -q origin; then
        git remote add origin git@github.com:CPUtester5465/Monitoring-docker.git
    fi

    git push -u origin "$file"#nameofbranch
else
    echo "Error" 
fi
# Waiting for the admin to add the local computer key to their account
# Copying the key to the remote server
ssh-copy-id -i ~/.ssh/"$file.pub" ubuntu@13.50.4.224 
