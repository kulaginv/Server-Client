# Server-Client

This project implements a system for sending, receiving and storing customer metrics.
The protocol supports two types of requests to the server from the client:
- sending data to save it on the server
- receiving saved data
## The general format of the client's request:
`<command> <request data><\n>`    
>
`<command>` - server command (the command can take one of two values: put - save data on the server, get - return saved data from the server   
`<\n>` - line break character  
`<request data>` - Your data to transmit and receive  

### Request data
For each metric (\<key>), data about its values (\<value>) and the time when the measurement was performed (\<timestamp>) will be stored.
