# mcts_connect4
Experiment Monte Carlo tree search with the Connect Four game

# Run it
Example: first player: human; second player: MCTS player with 30 seconds per move <br/>
&nbsp;&nbsp;&nbsp;&nbsp;./Connect4.py --p1 h --p2 m --p2time 30 <br/>
Run ./Connect4.py --help for details <br/>

# Unit test
Run all tests: ./runtests <br/>
Run individual tests: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;PYTHONPATH=\<code path>:\<code path>/tests <br/>
&nbsp;&nbsp;&nbsp;&nbsp;export PYTHONPATH <br/>
&nbsp;&nbsp;&nbsp;&nbsp;python -m unittest \<TestClass>[.\<TestCase>] <br/>

# Profile
python -m cProfile -o \<outputfile> ./Connect4.py ...<br/>
<br/>
With the current code, it can run a few thousands simulations per 30 seconds on a MacBook Pro with 2.7 GHz Intel Core i7, and 16G RAM.

# Change logging level
Edit Logging.conf

# See all games history
If you have kept one: open ./Connect4.log
