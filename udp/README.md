```
    Server                  Client
      |                        |
    bind()                     |
      |                        |
    recvfrom()  <--------   sendto()
      |                        |
    sendto()    <--------   recvfrom()
      |                        |
    close()                 close()
    
```
