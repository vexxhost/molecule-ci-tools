#!/usr/bin/env python

import errno
import os
import sys
import yaml

# If we're not running in CI, fail.
if not os.getenv('CONTINUOUS_INTEGRATION') and not os.getenv('JENKINS_URL'):
    sys.exit(errno.EINVAL)

# Select build number
build = "%s-%s" % (os.getenv('JOB_NAME'), os.getenv('BUILD_NUMBER'))
if build == 'None-None':
    build = os.getenv('TRAVIS_BUILD_NUMBER')
build = build.replace('/', '-')

# Add Prefix
prefix = ''
if len(sys.argv) == 2:
    prefix = "%s-" % sys.argv[1]

# Load configuration file
with open('molecule.yml', 'r') as fd:
    config = yaml.load(fd)

# Append the build number
for i in config['openstack']['instances']:
    i['name'] = "%s%s-%s" % (prefix, i['name'], build)

# Change molecule_dir so that it uses different keys
# https://github.com/metacloud/molecule/blob/master/molecule/driver/openstackdriver.py#L282-L285
# mc = config.get('molecule', {})
# mc['molecule_dir'] = ".molecule-%s" % build
# config['molecule'] = mc

# Create updated configuration file
data = yaml.dump(config)
with open('molecule.yml', 'w') as fd:
    fd.write(data)

# Print the configuration file
print data
