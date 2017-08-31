import subprocess
import fileinput
import os
import sys



def update_config_paths():
	find_output = subprocess.Popen(['find', '/', '-name', 'GSbSFZwWV1mig4vFSmbLW9iP8TfGfMYCPfHTqGcD'], stdout=subprocess.PIPE)
	project_path_raw, err = find_output.communicate()
	project_path = str(project_path_raw.decode('utf-8'))[:-42]

	os.system('sudo cp -a Reset\ Device/static_files/rc.local.aphost.template Reset\ Device/static_files/rc.local.aphost')
	os.system('sudo cp -a Reset\ Device/static_files/rc.local.apclient.template Reset\ Device/static_files/rc.local.apclient')
	os.system('sudo cp -a Reset\ Device/reset.py.template Reset\ Device/reset.py')

	with fileinput.FileInput("Reset Device/static_files/rc.local.aphost", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close
	
	with fileinput.FileInput("Reset Device/static_files/rc.local.apclient", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close
	
	with fileinput.FileInput("Reset Device/reset.py", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close


#################################################################
#################################################################


print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
run_setup_ans = input("Would you like to run the initial setup for RaspiWiFi? (y/n): ")

if(run_setup_ans == 'y'):
	print()
	print("Detecting RaspiWiFi location...")
	
	update_config_paths()
	
	os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm -f ./tmp/*')
	os.system('sudo cp -r ./Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
	os.system('sudo cp -r ./Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
	os.system('sudo cp -r ./Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
	os.system('sudo cp -r ./Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
	os.system('sudo cp -r ./Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
else:
	print()
	print()
	print("---------------------------------------------------")
	print("---------------------------------------------------")
	print("RaspiWiFi initial setup cancelled. No changes made.")
	sys.exit(0)

print()
print()
reboot_ans = input("Initial setup is complete. A reboot is required, would you like to do that now? (y/n): ")

if(run_setup_ans == 'y' and reboot_ans == 'y'):
	os.system('sudo reboot')
