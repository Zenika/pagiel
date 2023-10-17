import json
import sys

# get arguments
[_, host, strport, org, token, bucket] = sys.argv

# port is expecting an int
port = 0
try:
    port = int(strport)
except ValueError:
    print(f'Invalid port value: {strport}, must be an integer.')
    sys.exit(1)

try:
    # trying to read the default config file
    with open('sitespeed/config/config-default.json', encoding='utf8') as sitespeed_default_config_file:
        json_config = json.load(sitespeed_default_config_file)
    # customize the config
    json_config['influxdb']['host'] = host
    json_config['influxdb']['port'] = port
    json_config['influxdb']['database'] = bucket
    json_config['influxdb']['token'] = token
    json_config['influxdb']['organisation'] = org

    # create or overwrite the config file, no need for test
    with open('sitespeed/config/config.json', 'w', encoding='utf8') as sitespeed_config_file:
        json.dump(json_config, sitespeed_config_file)
        print('Sitespeed config saved.')
except FileNotFoundError:
    print('Default config file does not exist.')
    sys.exit(1)
except json.decoder.JSONDecodeError:
    print('Cannot read default config.')
    sys.exit(1)
