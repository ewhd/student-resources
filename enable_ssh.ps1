# from https://woshub.com/connect-to-windows-via-ssh/

# to download this script
#Invoke-WebRequest -Uri https://raw.githubusercontent.com/ewhd/student-resources/main/enable_ssh.ps1 -OutFile enable_ssh.ps1

# to enable powershell scripts:
#Set-ExecutionPolicy RemoteSigned

# install ssh-server
Get-WindowsCapability -Online | Where-Object Name -Like 'OpenSSH.Server*' | Add-WindowsCapability -Online

# check installation
Get-WindowsCapability -Online | ? name -Like 'OpenSSH.Ser*'

# change the startup type of the sshd service to automatic and start the service using PowerShell:
Set-Service -Name sshd -StartupType 'Automatic'
Start-Service sshd

#create firewall rule
#Get-NetFirewallRule -Name *OpenSSH-Server* |select Name, DisplayName, Description, Enabled
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
