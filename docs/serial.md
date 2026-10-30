## DALI frame format for serial input
  
Each DALI frame is expected to use the following format:

    "{" <timestamp> <marker> <bits> " " <data> "}"

Only information framed by curly braces is interpreted. <br/>

    <timestamp> : integer number, 
                each tick represents 1 millisecond, 
                number is given in hex presentation, 
                fixed length of 8 digits
    <marker>    : a single character, either a 
                ">" (greater than) indicating a loopback frame, which was transmitted by the interface itself, or 
                any other character, e.g. ":" (colon), indicating a frame received from the bus
    <bits>      : data bits received, 
                number is given in hex presentation, 
                fixed length of 2 digits
    <data>      : received data payload, 
                number is given in hex presentation, 
                up to 8 digits

Example: `{00000001:10 FF06}` is a 16 bit frame `FF06` received 1 ms after the start of the interface.

In case of an error state:<br/>

    <bits> : codes the error code
    <data> : contains additional error information

| Code `<bits>` | Meaning                                                                         |
|---------------|---------------------------------------------------------------------------------|
| 0x81          | timeout                                                                         |
| 0x82          | timing error in start bit, `<data>`: bit number (bits 0-7), time in µs (bits 8-27) |
| 0x83          | timing error in data bit, `<data>`: bit number (bits 0-7), time in µs (bits 8-27)  |
| 0x88          | corrupt frame                                                                   |
| 0x91          | system failure                                                                  |
| 0x92          | system recovered                                                                |
| 0xA0          | command not processed                                                           |
| 0xA2          | queue is full                                                                   |
| 0xA3          | bad command                                                                     |
| 0xA5          | DALI queue is full                                                              |

Other codes above 0x80 are reported as interface error with the code.
