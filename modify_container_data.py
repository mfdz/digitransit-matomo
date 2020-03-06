# Reads an exported Matomo Tag Manager version and changes the necessary fields to be import ready.

# Should run as MATOMO_IDCONTAINER=<> MATOMO_IDSITE=<> MATOMO_MATOMOURL=<> python modify_container_data.py <source_file_name>
# Variables should have the data of the container, you'd like to import into.
# idcontainer: ab1asf2f3
# idsite is usually 1
# matomourl: http://example.org

import json
import sys
import os

def main(argv):
	source_file = sys.argv[1]
	dest_file = "importReadyContainer.json"

	with open(source_file) as file:
	    data = json.load(file)

	data['idcontainer'] = os.getenv('MATOMO_IDCONTAINER', "")
	data['idsite'] = os.getenv('MATOMO_IDSITE', "")
	data['variables'][0]['parameters']['idSite'] = os.getenv('MATOMO_IDSITE', "")
	data['variables'][0]['parameters']['matomoUrl'] = os.getenv('MATOMO_MATOMOURL', "")

	with open(dest_file, "w") as f:
	    json.dump(data, f, indent=2)

main(sys.argv)