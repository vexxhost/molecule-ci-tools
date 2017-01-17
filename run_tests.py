#!/usr/bin/env python

import os
import sys

# Get path for current file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Run the tests
os.system("%s/setup_config.py" % dir_path)
ret = os.system("molecule test --destroy=always")
exit_code = os.WEXITSTATUS(ret)
sys.exit(exit_code)
