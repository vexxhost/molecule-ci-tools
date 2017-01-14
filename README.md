# Molecule CI tools
This repository contains a set of useful tools when using `molecule` to test
Ansible roles.  We've found those to be useful in our testing and especially
when doing it against our cloud.

## `run_tests.py`
`molecule` relies on the name of the server being the same on each run, which
means that you can only run one check at a time against a cloud tenant or other
wise your runs will clash.  This runner will override the `molecule` file just
before running it by adding a suffix with the build number.

It's currently hardcoded to the Travis-CI environment variables however it
should be straightforward to make that a parameter (contributions welcome!)
