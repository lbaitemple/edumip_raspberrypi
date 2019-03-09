#!/usr/bin/python
from collections import deque

c = deque(maxlen=4)
#c = circularlist(4)
c.append(1); print c, len(c), c[0], c[-1]    #[1] (1 items)              first 1, last 1
c.append(2); print c, c[0], c[-1]    #[1, 2] (2 items)           first 1, last 2
c.append(3); print c, c[0], c[-1]    #[1, 2, 3] (3 items)        first 1, last 3
c.append(8); print c, c[0], c[-1]    #[1, 2, 3, 8] (4 items)     first 1, last 8
c.append(10); print c, c[0], c[-1]   #[10, 2, 3, 8] (4 items)    first 2, last 10
c.append(11); print c, c[0], c[-1]   #[10, 11, 3, 8] (4 items)   first 3, last 11

