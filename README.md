# GNU Mailman3 utils

Lightweight utilities for common tasks.

[create_list.py](create_list.py) and [update_list.py](update_list.py) will apply their own, opinionated set of settings to the list (see `apply_list_settings` function in [common.py](common.py)). The other tools are generic.

This implementation is a thin wrapper around [Mailman Client](https://docs.mailman3.org/projects/mailmanclient/en/latest/).

# Example

```shell
$ export MAILMAN_REST_API_PASS=xxx
$ list_domains.py
lists.a.com
lists.b.com
lists.c.com
$ list_lists.py
thislist@lists.a.com
thatlist@lists.b.com
testlist@lists.b.com
```
