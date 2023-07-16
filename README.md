# traefik_add_to_config.yml
A small Python script that adds an entry to Routers and Services for a new service you want to reverse proxy.

Functionality:

The script will add a router/service for a new item you want to add to your dynamic config.yml (it will place new router/service alphabetically).

like this:
 
  Routers:
  
    plex:   
      entryPoints:
      - https
      rule: Host(`plex.mydomain.com`) 
      middlewares:
      - chain-no-auth
      tls: {}
      service: plex-svc
      
  Services: 
  
    plex-svc:
      loadBalancer:
        servers:
        - url: '"http://10.10.0.100:32400/"'
        passHostHeader: true
        
To run the code, you'll need to have the PyYAML package installed. You can install it using pip by running the following command:

pip install PyYAML

Note this script will only work with a yaml based config, not a toml based config.  I personally followed the instructions provided by Ibracorp at ibracrop.io to install traefik2 to my unraid server. 

link: https://docs.ibracorp.io/traefik/

To run the application, copy the script into your traefik config directory.  cd to that direcotry.  Note it is advisalbe to make a copy of your current config, and run the script on a copy of config.yml

Usage:

  root@Server:/mnt/user/appdata/traefik# python3 add_script.py ./config_copy.yml
  
  Enter the name of the application: myapp
  
  Enter the hostname for the application: example
  
  Enter the IP address of the service: 10.10.0.100:420
  
  Updated config file saved as config_updated.yaml
  
Bugs:

Please note: I am currently working on a bug that adds single and double-quotes around every ip address under:
   
    ServiceName-svc:
      loadBalancer:
        servers:
        - url: '"http://10.10.0.100:420/"'  this should be - url: "http://10.10.0.100:420/"
