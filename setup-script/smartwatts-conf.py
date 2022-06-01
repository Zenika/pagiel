import json
import sys

[_, host, strport, org, token, bucket] = sys.argv
port = 0
try:
    port = int(strport)
except ValueError:
    print("Port {} invalide".format(strport))
    sys.exit()

with open("smartwatts/config-default.json") as baseconfig:
    try:
        json_config = json.load(baseconfig)
    except json.decoder.JSONDecodeError:
        print("config par défaut illisible")
        sys.exit()
    json_config["output"]["pusher_power"]["uri"] = host
    json_config["output"]["pusher_power"]["port"] = int(port)
    json_config["output"]["pusher_power"]["bucket"] = bucket
    json_config["output"]["pusher_power"]["token"] = token
    json_config["output"]["pusher_power"]["org"] = org
    with open("smartwatts/config.json", "w") as config:
        json.dump(json_config, config)
        print("Smartwatt config saved")