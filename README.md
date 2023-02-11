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
7. Initially stored in memory - future in the file system

## Architecture

- Master volume will keep track of the stored keys
- Child volumes will store the actual data

## Redis protocol for communication

| Data-Type        |      Prefix      |                      Structure                    |                                                                                                         Example                                                                              |
|------------------|:----------------:|:-------------------------------------------------:|                                                                                                                                                    -----------------------------------------:|
| Simple String    |        +         | +{string data}\r\n                                | ``` +this is a simple string\r\n ```                                                                                                                                                         | 
| Error            |        -         | -{error message}\r\n                              | ``` -ERR unknown command "FLUHS"\r\n ```                                                                                                                                                     |
| Integer          |        :         | :{the number}\r\n                                 | ``` :1337\r\n ```                                                                                                                                                                            |
| Binary           |        $         | ${number of bytes}\r\n{data}\r\n                  | ``` $6\r\n ```<br>```foobar\r\n```                                                                                                                                                           |
| Array            |        *         | *{number of elements}\r\n{0 or more of above}\r\n | ``` *3\r\n ```<br>``` +a simple string element\r\n ```<br>``` :12345\r\n ```<br>``` $7\r\n ```<br>``` testing\r\n ```                                                                        |
| Dictionary       |        %         | %{number of keys}\r\n{0 or more of above}\r\n     | ```%3\r\n```<br>```+key1\r\n```<br>```+value1\r\n```<br>```+key2\r\n```<br>```*2\r\n 1```<br>```+value2-0\r\n```<br>```+value2-1\r\n```<br>```:3\r\n```<br>```$7\r\n```<br>```testing\r\n``` |
| NULL             |        $         | $-1\r\n (string of length -1)                     | ``` $-1\r\n ```                                                                                                                                                                              |
    