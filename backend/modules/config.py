import yaml

with open('config.yaml', 'r') as ymlfile:
	cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def get(key):
	return cfg[key]