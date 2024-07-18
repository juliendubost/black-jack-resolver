
```text

Black Jack resolver

 _ _   _ _ 
| A | | J |
| _ | | _ |
```

Black Jack resolver give the hit equity for each player state and bank card.

# Install using poetry


```shell
poetry install
```

# Usage in a python shell 

Activate poetry env then run ipython

```shell
poetry shell
ipython
```

```python
from blackjack.constants import HandState
from blackjack.graph import PlayerGraph

# Build player graph for bank card 7 then display it
pg = PlayerGraph(HandState.SEVEN)
pg.build()
print(pg)

"""
-------------------------------------------------
Bank card: 7
-------------------------------------------------
Player state        EV stand       EV hit & stand 
-------------------------------------------------
2                   0.525          0.525          
3                   0.525          0.525          
4                   0.525          0.525          
5                   0.525          0.525          
6                   0.525          0.553          
7                   0.525          0.705          
8                   0.525          0.906          
9                   0.525          1.052          
10                  0.525          1.196          
F                   0.525          1.24           
11                  0.525          1.231          
12                  0.525          0.747          
13                  0.525          0.706          
14                  0.525          0.666          
15                  0.525          0.626          
16                  0.525          0.585          
17                  0.893          0.517          
18                  1.4            0.409          
19                  1.616          0.285          
20                  1.773          0.148          
A                   0.525          1.408          
2-12                0.525          0.908          
3-13                0.525          0.908          
4-14                0.525          0.908          
5-15                0.525          0.908          
6-16                0.525          0.908          
7-17                0.893          0.993          
8-18                1.4            1.11           
9-19                1.616          1.16           
10-20               1.773          1.196          
21                  1.926          0              
1-1                 0.525          0.908          
2-2                 0.525          0.525          
3-3                 0.525          0.553          
4-4                 0.525          0.906          
5-5                 0.525          1.196          
6-6                 0.525          0.747          
7-7                 0.525          0.666          
8-8                 0.525          0.585          
9-9                 1.4            0.409          
10-10               1.773          0.148          
BJ                  2.5            0              
-------------------------------------------------

"""
```





