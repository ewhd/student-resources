# A script of all the commands I ran to get my lab set-up
# This is not necessarily tested -- it's more like live notes of my process which *might* run as a script
# Some of this I cribbed from https://github.com/lee5378/labsetup/blob/main/labsetup.sh

# Deactivate screen locking, since we're mostly running this as a headless server box via RDP
gsettings set org.gnome.desktop.screensaver lock-enabled false

cd ~/Downloads
touch deployerlog.txt

sudo apt update
sudo apt-get update
sudo apt upgrade -y

# Install Open SSH Server, allow firewall, and launch the service on startup
sudo apt-get install openssh-server -y
sudo systemctl start sshd
sudo ufw allow ssh
sudo systemctl enable ssh

# Install curl
sudo apt install curl -y
curl --version >> ~/Downloads/deployerlog.txt

# Install VS Code
sudo apt install software-properties-common apt-transport-https wget -y
# this next line needed some modification/updating: https://www.linuxuprising.com/2021/01/apt-key-is-deprecated-how-to-add.html
# wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo tee /usr/share/keyrings/microsoft-archive-keyr
ing.gpg
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt install code -y
code --version >> ~/Downloads/deployerlog.txt 

# Install KVM/QEMU
# https://computingforgeeks.com/install-kvm-hypervisor-on-ubuntu-linux/
sudo apt update
sudo apt -y install qemu-kvm libvirt-daemon bridge-utils virtinst libvirt-daemon-system
# Also install other useful Virtual Machine management tools.
# This will give you tools similar to Linux ls, cat, top command for use with Virtual Machines.
sudo apt -y install virt-top libguestfs-tools libosinfo-bin  qemu-system virt-manager
sudo modprobe vhost_net 
echo vhost_net | sudo tee -a /etc/modules
kvm --version >> ~/Downloads/deployerlog.txt

# Install Terraform
# https://computingforgeeks.com/how-to-install-terraform-on-linux/
TER_VER=`curl -s https://api.github.com/repos/hashicorp/terraform/releases/latest | grep tag_name | cut -d: -f2 | tr -d \"\,\v | awk '{$1=$1};1'`
wget https://releases.hashicorp.com/terraform/${TER_VER}/terraform_${TER_VER}_linux_amd64.zip

# Install Terraform KVM provider
# The Terraform KVM provider will provision infrastructure with Linux’s KVM using libvirt.
cd ~
terraform init
cd ~/.terraform.d
mkdir plugins
curl -s https://api.github.com/repos/dmacvicar/terraform-provider-libvirt/releases/latest \
  | grep browser_download_url \
  | grep linux_amd64.zip \
  | cut -d '"' -f 4 \
  | wget -i -
unzip terraform-provider-libvirt_*_linux_amd64.zip
rm -f terraform-provider-libvirt_*_linux_amd64.zip
mkdir -p ~/.terraform.d/plugins/
mv terraform-provider-libvirt_* ~/.terraform.d/plugins/terraform-provider-libvirt
echo "terraform {
  required_providers {
    libvirt = {
      source = \"dmacvicar/libvirt\"
    }
  }
}

provider \"libvirt\" {
  # Configuration options
  uri = "qemu:///system"
  #alias = "server2"
  #uri   = "qemu+ssh://root@192.168.100.10/system"
}" >> main.tf



# Wrapup
echo "Deployment script completed. Here's what is now installed:"
cat ~/Downloads/deployerlog.txt