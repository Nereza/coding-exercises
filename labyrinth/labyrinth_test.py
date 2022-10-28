import io
import unittest
import sys
from unittest.mock import patch, mock_open

import labyrinth as candidate


class TestLabyrinthEscape(unittest.TestCase):

    ESCAPED = 'Entkommen in {} Minute(n)!\n'
    TRAPPED = 'Gefangen :-(\n'

    def test_escape_one_layer(self):
        with patch('labyrinth.open', new=mock_open(read_data="""1 3 3
S.#
#..
.#E

0 0 0""")) as _file:
            output = io.StringIO()
            sys.stdout = output
            candidate.escape_labyrinths('mockfile')
            sys.stdout = sys.__stdout__
            self.assertEqual(self.ESCAPED.format(4), output.getvalue())

    def test_no_escape_one_layer(self):
        with patch('labyrinth.open', new=mock_open(read_data="""1 3 3
S##
#.#
.#E

0 0 0""")) as _file:
            output = io.StringIO()
            sys.stdout = output
            candidate.escape_labyrinths('mockfile')
            sys.stdout = sys.__stdout__
            self.assertEqual(self.TRAPPED, output.getvalue())

    def test_escape_one_layer_10x10(self):
        with patch('labyrinth.open', new=mock_open(read_data="""1 10 10
##########
#......#.#
#.##.###.#
#S##.###E#
#.#......#
#.######.#
#.######.#
#.##.###.#
#.##.###.#
#........#

0 0 0""")) as _file:
            output = io.StringIO()
            sys.stdout = output
            candidate.escape_labyrinths('mockfile')
            sys.stdout = sys.__stdout__
            self.assertEqual(self.ESCAPED.format(13), output.getvalue())

    def test_two_labyrinths(self):
        with patch('labyrinth.open', new=mock_open(read_data="""1 3 3
S##
#.#
.#E

1 3 3
##S
#..
.#E

0 0 0""")) as _file:
            output = io.StringIO()
            sys.stdout = output
            candidate.escape_labyrinths('mockfile')
            sys.stdout = sys.__stdout__
            self.assertEqual(self.TRAPPED + self.ESCAPED.format(2), output.getvalue())

    def test_escape_multiple_layers_10x10(self):
        with patch('labyrinth.open', new=mock_open(read_data="""5 10 10
##########
##########
##########
##.#######
##.#######
##.....###
##.##...##
##..######
###..####
####.#####

##########
####.#####
####.#####
##...#####
##########
##########
##########
##########
##.#######
##......##

##########
##S..#####
##########
##########
##########
##########
...#######
##.###E..#
##.#######
##########

#######.##
#######.##
....###..#
.#######.#
.#######.#
.#######.#
.#######.#
########.#
##########
##########

#####...##
#####.####
###.#.####
###.#.####
###.#.####
###...####
##########
##########
##########
##########

0 0 0""")) as _file:
            output = io.StringIO()
            sys.stdout = output
            candidate.escape_labyrinths('mockfile')
            sys.stdout = sys.__stdout__
            self.assertEqual(self.ESCAPED.format(58), output.getvalue())
