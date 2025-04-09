from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'ip' : '172.20.10.5',
    'username' : 'admin',
    'password' : 'eve',
}

net_connect = ConnectHandler(**device)
output = net_connect.send_command('sh run')
