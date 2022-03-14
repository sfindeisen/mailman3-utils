# GNU Mailman3 utils

Basic utilities for common tasks.

This implementation is a wrapper around [Mailman Client](https://docs.mailman3.org/projects/mailmanclient/en/latest/).

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
