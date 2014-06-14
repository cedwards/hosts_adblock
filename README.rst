hosts_adblock
-------------

REQUIRES: sessions (pip install sessions)

This script generates an /etc/hosts file for ad blocking. Currently
pulls in lists from:

http://hosts-file.net
http://pgl.yoyo.org/as/
http://winhelp2002.mvps.org/hosts.htm

The total list is just over 32,000 lines, and should not include any
duplicates. This is one of my first Python scripts, so pull requests
with improvements are welcome.

usage
-----

  python2 generate_hosts.py

This will create a 'hosts' file in the current directory after merging
the three lists. Append this generated file to your existing ``/etc/hosts``.
Browsers may need to be restarted for changes to take effect.

You'll still probably want to use Adblock browser plugin to remove empty
elements.
