T1 18 fffe1d # start quiescent mode
S1 10 a100   # terminate
T1 10 a500   # iniatialize (all)
S1 10 a3ff   # data transfer register = 0xff
T1 10 ff80   # store dtr as short address
T1 10 a700   # randomize
S1 10 ff70   # remove from group 0
S1 10 ff71   # remove from group 1
S1 10 ff72   # remove from group 2
S1 10 ff73   # remove from group 3
S1 10 ff74   # remove from group 4
S1 10 ff75   # remove from group 5
S1 10 ff76   # remove from group 6
S1 10 ff77   # remove from group 7
S1 10 ff78   # remove from group 8
S1 10 ff79   # remove from group 9
S1 10 ff7a   # remove from group 10
S1 10 ff7b   # remove from group 11
S1 10 ff7c   # remove from group 12
S1 10 ff7d   # remove from group 13
S1 10 ff7e   # remove from group 14
S1 10 ff7f   # remove from group 15
T1 10 a100   # terminate
