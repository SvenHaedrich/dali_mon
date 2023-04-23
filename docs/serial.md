## DALI frame format for serial input
  
Each DALI frame is expected to use the following format:

    "{" <timestamp> <error> <bits> " " <data> "}"

Only information framed by curly braces is interpreted. <br/>

    <timestamp> : integer number, 
                each tick represents 1 millisecond, 
                number is given in hex presentation, 
                fixed length of 8 digits
    <error>     : either a 
                "-" (minus) indicating normal state, or 
                "*" (asteriks) inidcating an error
    <bits>      : data bits received, 
                number is given in hex presentation, 
                fixed length of 2 digits
    <data>      : received data payload, 
                number is given in hex presentation, 
                fixed length of 8 digits

In case of an error state:<br/>

    <bits> : codes the error code
    <data> : contains additional error information
