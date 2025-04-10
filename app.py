# network_config_tool.py
import streamlit as st
import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, AuthenticationException

st.title("🔧 Cisco Sw, Router Tools")


#dropdown device type

band_device = st.selectbox("Band Device", [
    "Cisco", 
    "Juniper", 
    "Huawei",
    ])

if band_device == "Cisco":
    device_type = st.selectbox("Device Type", [
        "cisco_ios",
        "cisco_asa",
        "cisco_nxos",
        "cisco_iosxr",
    ])
elif band_device == "Juniper":
    device_type = st.selectbox("Device Type", [
        "juniper",
        "juniper_junos",
    ])
    
elif band_device == "Huawei":
    device_type = st.selectbox("Device Type", [
        "huawei",
        "huawei_vrp",
    ])
    


# input fields
ip = st.text_input("IP Address")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
commands = st.text_area("Configuration Commands (1 per line)", height=200)


if st.button("🚀 Send Config"):
    if not ip or not username or not password or not commands:
        st.warning("Fill in all fields")
    else:
        try:
            device = {
                'device_type': device_type,
                'ip': ip,
                'username': username,
                'password': password,
            }

            net_connect = ConnectHandler(**device)
            net_connect.enable()

            cmd_list = commands.strip().split('\n')
            output = net_connect.send_config_set(cmd_list)

            st.success("✅ config sent successfully")
            st.code(output, language="bash")

            # save config
            net_connect.save_config()

        except AuthenticationException:
            st.error("❌ Authentication Failed! pls check username/password")
        except NetMikoTimeoutException:
            st.error("❌ Timeout! Unable to connect to device")
        except Exception as e:
            st.error(f"Error: {str(e)}")

#backup config
if st.button("📥 Backup Config"):
    if not ip or not username or not password:
        st.warning("fill in all fields")
    else:
        try:
            device = {
                'device_type': 'cisco_ios',
                'ip': ip,
                'username': username,
                'password': password,
            }

            net_connect = ConnectHandler(**device)
            net_connect.enable()

            command = ['show running-config', 'show ip int br', 'show version']
            name_command = ['running-config', 'ip-int-br', 'version']

            for i, cmd in enumerate(command):
                output = net_connect.send_command(cmd)
                filename = f"backup_{name_command[i]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, "w") as file:
                    file.write(output)

                st.success(f"✅ save config -> {filename}")

        except AuthenticationException:
            st.error("❌ Authentication Failed! pls check username/password")
        except NetMikoTimeoutException:
            st.error("❌ Timeout! Unable to connect to device")
        except Exception as e:
            st.error(f"Error: {str(e)}")