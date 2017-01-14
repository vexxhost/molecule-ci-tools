#!/usr/bin/env python

import errno
import os
import sys
import yaml

from molecule.config import ConfigV1

# If we're not running in CI, fail.
if os.getenv('CONTINUOUS_INTEGRATION') != 'true':
    sys.exit(errno.EINVAL)

# Get config and suffix with build number
c = ConfigV1()
for i in c.config['openstack']['instances']:
    i['name'] = "%s-%s" % (i['name'], os.getenv('TRAVIS_BUILD_NUMBER'))

# Change molecule_dir so that it uses different keys
# https://github.com/metacloud/molecule/blob/master/molecule/driver/openstackdriver.py#L282-L285
c.config['molecule']['molecule_dir'] = "%s-%s" % (c.config['molecule']['molecule_dir'], os.getenv('TRAVIS_BUILD_NUMBER'))
    
# Create updated configuration file
data = yaml.dump(c.config)
with open('molecule.yml', 'w') as fd:
    fd.write(data)

# Run the tests
ret = os.system("molecule test --destroy=always")
exit_code = os.WEXITSTATUS(ret)
sys.exit(exit_code)
