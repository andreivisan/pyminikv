# SIMPLE DISTRIBUTED DATABASE SERVER

## Requirements

1. Database server under 1000 lines of code
2. Key/Value support
3. Distributed DB server using [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html)
4. Initial build in Python - future build in Go to improve performance
5. Server will respond to following commands

    - GET <key>
    - SET <key> <value>
    - DELETE <key>
    - FLUSH
    - MGET <key1> ... <keyn>
    - MSET <key1> <value1> ... <keyn> <valuen>
6. Supported data types
    - Strings and Binary Data
    - Numbers
    - NULL
    - Arrays (which may be nested)
    - Dictionaries (which may be nested)
    - Error messages