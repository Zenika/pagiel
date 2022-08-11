import json
import sys

# get arguments
[_, host, strport, org, token, bucket] = sys.argv

# port is expecting an int
port = 0
try:
    port = int(strport)
except ValueError:
    print("Invalid port value : {}.".format(strport))
    sys.exit()

# trying to read the default config file
try:
    default_file = open("smartwatts/config-default.json")
except FileNotFoundError:
    print("Default config file do not exists.")
    sys.exit()
else: 
    with default_file:
        try:
            json_config = json.load(default_file)
        except json.decoder.JSONDecodeError:
            print("Can't read default config.")
            sys.exit()
            
        # saving good config
        json_config["output"]["pusher_power"]["uri"] = f"http://{host}"
        json_config["output"]["pusher_power"]["port"] = int(port)
        json_config["output"]["pusher_power"]["db"] = bucket
        json_config["output"]["pusher_power"]["token"] = token
        json_config["output"]["pusher_power"]["org"] = org

        # create or overwrite the file, no need for test
        with open("smartwatts/config.json", "w") as config:
            json.dump(json_config, config)
            print("Smartwatt config saved.")