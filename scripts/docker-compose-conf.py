import yaml
import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description = "Convert user url request to required file format from container")
    parser.add_argument("inputFile", help="User docker-compose file")
    parser.add_argument("network", help="pagiel default network")
    return parser.parse_args()

def load_yaml_file(filename):
    with open(filename) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def save_yaml_file(file_name: str, compose_dict: dict):
    with open(file_name, 'w') as file:
        yaml.dump(compose_dict, file)

def add_pagiel_network(compose_dict, network_name):
    compose_dict["networks"] = {'default': {'external': {'name': network_name}}}

def strip_services_args(compose_dict):
    for container_options in compose_dict["services"].values():
        container_options.pop('ports', None)

def main():
    args = parse_args()
    dockerfile = load_yaml_file(args.inputFile)
    add_pagiel_network(dockerfile, args.network)
    strip_services_args(dockerfile)
    save_yaml_file(args.inputFile, dockerfile)

if __name__ == "__main__":
    main()