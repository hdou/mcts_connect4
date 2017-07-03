# mcts_connect4
Experiment Monte Carlo tree search with a connect four game

# Run it
Example: first player: human; second player: MCTS player with 30 seconds per move <br/>
&nbsp;&nbsp;&nbsp;&nbsp;./Connect4.py --p1 h --p2 m --p2time 30 <br/>
Run ./Connect4.py --help for details <br/>

# Unit test
Run all tests: ./runtests <br/>
Run individual tests: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;PYTHONPATH=\<code path>:\<codepath>\\tests <br/>
&nbsp;&nbsp;&nbsp;&nbsp;export PYTHONPATH <br/>
&nbsp;&nbsp;&nbsp;&nbsp;python -m unittest \<TestClass>[.\<TestCase>] <br/>

# Profile
python -m cProfile -o \<outputfile> ./Connect4.py ...

# Change logging level
Edit Logging.conf

# See all games history
If you have kept one: open ./Connect4.log
