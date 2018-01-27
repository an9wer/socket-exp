```
    Server                  Client
      |                        |
    bind()                     |
      |                        |
    listen()                   |
      |                        |
    accept()    <--------   connect()
      |                        |
    read()      <--------   write()
      |                        |
    write()     <--------   read()
      |                        |
    close()                 close()
    
```
