# GNU Mailman3 utils

Lightweight utilities for common tasks.

[create_list.py](create_list.py) and [update_list.py](update_list.py) will apply their own, opinionated set of settings to the list (see `apply_list_settings` function in [common.py](common.py)). The rest of this code is generic.

This implementation is a thin wrapper around [Mailman Client](https://docs.mailman3.org/projects/mailmanclient/en/latest/).

# How to run

First, extract `admin_pass` for your site from the configuration file and set `MAILMAN_REST_API_PASS` environment variable. For example:

```shell
$ grep admin_pass /etc/mailman3/mailman.cfg
$ export MAILMAN_REST_API_PASS=xxx
```

Then run the scripts:

```shell
$ list_domains.py
lists.a.com
lists.b.com
lists.c.com
$ list_lists.py
thislist@lists.a.com
thatlist@lists.b.com
testlist@lists.b.com
```
