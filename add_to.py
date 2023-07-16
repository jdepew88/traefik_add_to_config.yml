import sys
import yaml

# Get the path to the config_copy.yml file from the command-line argument
config_file = sys.argv[1]

# Load the existing dynamic config from the config_copy.yml file
with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

# Get input from the user
app_name = input("Enter the name of the application: ")
hostname = input("Enter the hostname for the application: ")
ip_address = input("Enter the IP address of the service: ")

# Create the new router entry
router_entry = {
    'entryPoints': ['https'],
    'rule': f'Host(`{hostname}.mydomain.com`)',
    'middlewares': ['chain-no-auth'],
    'tls': {},
    'service': f'{app_name.lower()}-svc'
}

# Create the new service entry
service_entry = {
    'loadBalancer': {
        'servers': [{'url': f"http://{ip_address}/"}],
        'passHostHeader': True
    }
}

# Insert the new router entry in alphabetical order
routers = config['http']['routers']
routers[app_name.lower()] = router_entry
config['http']['routers'] = dict(sorted(routers.items()))

# Insert the new service entry in alphabetical order
services = config['http']['services']
services[f'{app_name.lower()}-svc'] = service_entry

# Add double quotes around the URL in all service entries
for service_data in config['http']['services'].values():
    for server_data in service_data['loadBalancer']['servers']:
        server_data['url'] = f'"{server_data["url"]}"'

# Sort the services in alphabetical order
sorted_services = dict(sorted(services.items()))

# Rearrange the sections
config['http']['services'] = sorted_services

# Save the updated config file as "config_updated.yaml"
output_file = "config_updated.yaml"
with open(output_file, 'w') as file:
    yaml.dump(config, file, sort_keys=False, default_flow_style=False)

print(f"Updated config file saved as {output_file}")
