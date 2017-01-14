#!/usr/bin/env python

import errno
import os
import sys
import yaml

# If we're not running in CI, fail.
if os.getenv('CONTINUOUS_INTEGRATION') != 'true':
    sys.exit(errno.EINVAL)

# Load configuration file
with open('molecule.yml', 'r') as fd:
    config = yaml.load(fd)

# Append the build number
for i in config['openstack']['instances']:
    i['name'] = "%s-%s" % (i['name'], os.getenv('TRAVIS_BUILD_NUMBER'))

# Change molecule_dir so that it uses different keys
# https://github.com/metacloud/molecule/blob/master/molecule/driver/openstackdriver.py#L282-L285
mc = config.get('molecule', {})
mc['molecule_dir'] = ".molecule-%s" % os.getenv('TRAVIS_BUILD_NUMBER')
config['molecule'] = mc

# Create updated configuration file
data = yaml.dump(config)
with open('molecule.yml', 'w') as fd:
    fd.write(data)

# Print the configuration file
print config

# Run the tests
ret = os.system("molecule test --destroy=always")
exit_code = os.WEXITSTATUS(ret)
sys.exit(exit_code)
