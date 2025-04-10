import datetime
from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'ip' : '172.20.10.5',
    'username' : 'admin',
    'password' : 'eve',
}

net_connect = ConnectHandler(**device)


net_connect.enable()

# config commands

config_commands = [
    'interface ethernet 0/3',
    'ip address 192.168.1.1 255.255.255.192',
    'no shutdown'
]

net_connect.save_config()
net_connect.send_config_set(config_commands)

# check if the device is reachable
try:
    net_connect.find_prompt()
except Exception as e:
    print(f"Error: {e}")
    exit(1)


# save config to a file
command = ['show running-config', 'show ip int br', 'show version']
name_command = ['running-config', 'ip-int-br', 'version']
for i,cmd in enumerate(command):
    output = net_connect.send_command(cmd)
    filename = f"backup_{name_command[i]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as file:
        file.write(output)

    print(f"Saved config to {filename}")
