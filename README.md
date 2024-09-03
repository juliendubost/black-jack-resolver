```text
                 ... Black Jack Resolver ...
                 
                            _ _   
                           | A | 
                           | _ | 
                         bank card
                           
                     _ _                _ _
                 _ _| J |           _ _| K | 
                | A | _ |          | Q | _ |
                | _ |              | _ |
                            _ _     [Stand]  
                         _ _| 2 | 
                        | 5 | _ |                   
                        | _ |   
                          [Hit]

```

# Description

Black Jack resolver is a simple python app that compute and display expected values and best player move for each bank's start cards

Solving is determinist and based on a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) representation of hand states
A monte-carlo validation is implemented as unit tests to check some pre-computed values. Not the whole game have been modeled using a montecarlo validation

Hypothesis are:
- An infinite number of decks, at any time the probability of drawing card that is not ten-valued is 1/13 and 4/13 for a 10-valued card. Impact of this is judged insignificant as long as the house plays with 4+ decks
- No possibility to double after a split, this is not yet implemented because the impact on EV is judged as very low
- Dealer's peeked or not, controllable through a command line option. Dealer's peeked is mostly use in America where dealer stop the game before serving players if the face down card would reveal a blackjack
- Hit on soft 17 or not, controllable through a command line option.
- No limitations when you split a pair of Ace, you can still hit cards or make a blackjack after the split (most french casinos limit aces split to only 1 card and no blackjack)

Here are the computed game expected values depending on house rules, using the best strategy:

| dealer's peeked    | hit on soft 17       | This resolver strategy EV | 
|--------------------|----------------------|---------------------------|
|                    |                      | 1.00206                   | 
| X                  |                      | 1.012566                  |   
|                    | X                    | 1.000686                  | 
| X                  | X                    | 1.010486                  | 

`* using the case where double after a split is not allowed`

All best moves and expected values tables computable using this resolver are available in the `tables` directory.

# EV tables

Best moves table (see below) is issued from the EV tables for each bank card and player's start hand probabilities (see the `START_HAND_WEIGHTS` variable in `blackjack/constants.py`)

EV table approach is to compute, for each possible state:
- the standing EV
- the EV of hitting only 1 card then standing
- the maximum EV you can reach from this state using the best strategy

In the example below, best move is to surrender, because:
- the maximum EV you can reach from this state is `0.493`.
- if you stand, EV is `0.231`
- if you surrender, you get an EV of `0.5` (dealer take half of your bet) 

Consequently, best move is to surrender if possible, else hit.
```text
-------------------------------------------------------------------------------
Player state        EV stand       EV hit & stand      Max EV         Best move      
-------------------------------------------------------------------------------
12                  0.231          0.437               0.493          U-H   
```

In the other example, best move is to double if possible, else stand, because:
- stand EV is `0.828`
- max EV is `1.154`, net gain is `0.154`
- hit only 1 card then stand EV is `1.118`, net gain if you double from here is 2 times `0.118` = `0.236`

Consequently, because `0.236` is greater than `0.154` the maximum net gain is obtained using a double strategy.

If the EV of hitting only 1 card and standing would have been lesser than `0.154`, best move would have be to hit.


```text
-------------------------------------------------------------------------------
Player state        EV stand       EV hit & stand      Max EV         Best move      
-------------------------------------------------------------------------------
9                   0.828          1.118               1.154          D-H            
```

# Contributions

If you want to contribute, feel free to suggest and/or ask any questions.

Here are some ideas of things that could be done: 
- an external review of this code base to validate the approach.
- a full montecarlo game model to validate strategy expected values.
- a way to estimate the game variance to determine how many hands should be played to ensure player have a good chance to be wining.


# Install using poetry

```shell
poetry install
```

# Run tests

```shell
pytest  # run on a single thread
pytest -s  # run on a single thread and display logs
pytest -n 8  # run on 8 cores using pytest-xdist
```

# Usage 
Activate poetry env

```shell
poetry shell
```

Then run `jack.py` to display expected values for a given bank card or best moves table

For example, to display best moves table and strategy total expected value, use:

```shell
python jack.py best_moves
```

Default is to have the dealer's peeked option and stand on soft 17 .

This can be changed options `--no-peek` (disable dealer's peeked) and `--hos` (activate hit on soft 17) options.

Example output for standard use case (no hit on soft 17 and dealer peeked): 

```text
-----------------------------------------------------------------------------------
Player best move for each bank card (first line) and each state (first column)
-----------------------------------------------------------------------------------
	2	3	4	5	6	7	8	9	F	A	
-----------------------------------------------------------------------------------
20	S	S	S	S	S	S	S	S	S	S	
19	S	S	S	S	S	S	S	S	S	S	
18	S	S	S	S	S	S	S	S	S	S	
17	S	S	S	S	S	S	S	S	S	U-S	
16	S	S	S	S	S	H	H	U-H	U-H	U-H	
15	S	S	S	S	S	H	H	H	H	U-H	
14	S	S	S	S	S	H	H	H	H	U-H	
13	S	S	S	S	S	H	H	H	H	U-H	
12	H	H	S	S	S	H	H	H	H	U-H	
11	D-H	D-H	D-H	D-H	D-H	D-H	D-H	D-H	D-H	H	
10	D-H	D-H	D-H	D-H	D-H	D-H	D-H	D-H	H	H	
9	H	D-H	D-H	D-H	D-H	H	H	H	H	H	
8	H	H	H	H	H	H	H	H	H	H	
7	H	H	H	H	H	H	H	H	H	H	
6	H	H	H	H	H	H	H	H	H	H	
5	H	H	H	H	H	H	H	H	H	H	
4	H	H	H	H	H	H	H	H	H	H	
-----------------------------------------------------------------------------------
10-20	S	S	S	S	S	S	S	S	S	S	
9-19	S	S	S	S	S	S	S	S	S	S	
8-18	S	D-S	D-S	D-S	D-S	S	S	H	H	H	
7-17	H	D-H	D-H	D-H	D-H	H	H	H	H	H	
6-16	H	H	D-H	D-H	D-H	H	H	H	H	H	
5-15	H	H	H	D-H	D-H	H	H	H	H	H	
4-14	H	H	H	D-H	D-H	H	H	H	H	H	
3-13	H	H	H	H	D-H	H	H	H	H	H	
2-12	H	H	H	H	H	H	H	H	H	H	
-----------------------------------------------------------------------------------
1-1	Sp	Sp	Sp	Sp	Sp	Sp	Sp	Sp	Sp	Sp	
10-10	S	S	S	S	S	S	S	S	S	S	
9-9	Sp	Sp	Sp	Sp	Sp	S	Sp	Sp	S	S	
8-8	Sp	Sp	Sp	Sp	Sp	Sp	Sp	Sp	Sp	U-H	
7-7	Sp	Sp	Sp	Sp	Sp	Sp	H	H	H	U-H	
6-6	H	Sp	Sp	Sp	Sp	H	H	H	H	U-H	
5-5	D-H	D-H	D-H	D-H	D-H	D-H	D-H	D-H	H	H	
4-4	H	H	H	H	H	H	H	H	H	H	
3-3	H	H	Sp	Sp	Sp	Sp	H	H	H	H	
2-2	H	H	Sp	Sp	Sp	Sp	H	H	H	H	
-----------------------------------------------------------------------------------
legend:
	S: Stand
	H: Hit
	Sp: Split
	D-S: Double if possible else stand
	D-H: Double if possible else hit
	U-S: Surrender if possible else stand
	U-H: Surrender if possible else hit
	U-Sp: Surrender if possible else split
-----------------------------------------------------------------------------------
Total expected value using this strategy if double, split and surrender are allowed is: 1.00715
(you win a total of 1.00715 every time you do an initial bet of 1)
-----------------------------------------------------------------------------------
```


To display expected values table for an Ace on the bank, use:

```text
python jack.py --ev-table -card A
```

Possible values are: `2`, `3`,`4`,`5`,`6`,`7`,`8`,`9`,`F` (a ten-valued card),  

Output:

```text
-------------------------------------------------------------------------------
Bank card: A
-------------------------------------------------------------------------------
Player state        EV stand       EV hit & stand      Max EV         Best move      
-------------------------------------------------------------------------------
2                   0.231          0.231               0.552          H              
3                   0.231          0.231               0.535          H              
4                   0.231          0.231               0.517          H              
5                   0.231          0.231               0.502          H              
6                   0.231          0.241               0.482          U-H            
7                   0.231          0.301               0.478          U-H            
8                   0.231          0.412               0.556          H              
9                   0.231          0.542               0.647          H              
10                  0.231          0.687               0.749          H              
F                   0.231          0.742               0.803          H              
11                  0.231          0.73                0.791          H              
12                  0.231          0.405               0.45           U-H            
13                  0.231          0.387               0.418          U-H            
14                  0.231          0.37                0.388          U-H            
15                  0.231          0.352               0.36           U-H            
16                  0.231          0.334               0.334          U-H            
17                  0.361          0.306               0.361          U-S            
18                  0.623          0.259               0.623          S              
19                  0.885          0.191               0.885          S              
20                  1.146          0.102               1.146          S              
A                   0.231          0.948               1.117          H              
2-12                0.231          0.476               0.678          H              
3-13                0.231          0.476               0.653          H              
4-14                0.231          0.476               0.627          H              
5-15                0.231          0.476               0.602          H              
6-16                0.231          0.476               0.578          H              
7-17                0.361          0.506               0.568          H              
8-18                0.623          0.567               0.628          H              
9-19                0.885          0.627               0.885          S              
10-20               1.146          0.687               1.146          S              
21                  1.331          0                   1.331          S              
1-1                 0.231          0.476               0.678          Sp             
2-2                 0.231          0.231               0.517          H              
3-3                 0.231          0.241               0.482          U-H            
4-4                 0.231          0.412               0.556          H              
5-5                 0.231          0.687               0.749          H              
6-6                 0.231          0.405               0.45           U-H            
7-7                 0.231          0.37                0.388          U-H            
8-8                 0.231          0.334               0.334          U-H            
9-9                 0.623          0.259               0.623          S              
10-10               1.146          0.102               1.146          S              
BJ                  2.038          0                   2.038          S       
-------------------------------------------------------------------------------
Legend:
  [Player state] State of player game:
    10: a score of ten that can't lead to a black jack, for example 8 & 2 or 5 & 5 or 6 & 4, ...
    F: a single figure, this can be obtained only by splitting a pocket figure hand
  [EV stand] Give the expected value of standing in this position (1.0 = even)
  [EV hit & stand] Give the expected value of hit and stand from this position (useful to evaluate if a double is relevant)
  [Max EV] Give the maximum expected value that can be obtained from this position using only stand or hit choices
  [Best move] Give the best move from this position:
    S: Stand
    H: Hit
    Sp: Split
    D-S: Double if possible else stand
    D-H: Double if possible else hit
    U-S: Surrender if possible else stand
    U-H: Surrender if possible else hit
    U-Sp: Surrender if possible else split
-------------------------------------------------------------------------------
```
