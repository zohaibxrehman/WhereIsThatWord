""" Where's That Word? functions. """

# The constant describing the valid directions. These should be used
# in functions get_factor and check_guess.
UP = 'up'
DOWN = 'down'
FORWARD = 'forward'
BACKWARD = 'backward'

# The constants describing the multiplicative factor for finding a
# word in a particular direction.  This should be used in get_factor.
FORWARD_FACTOR = 1
DOWN_FACTOR = 2
BACKWARD_FACTOR = 3
UP_FACTOR = 4

# The constant describing the threshold for scoring. This should be
# used in get_points.
THRESHOLD = 5
BONUS = 12

# The constants describing two players and the result of the
# game. These should be used as return values in get_current_player
# and get_winner.
P1 = 'player one'
P2 = 'player two'
P1_WINS = 'player one wins'
P2_WINS = 'player two wins'
TIE = 'tie game'

# The constant describing which puzzle to play. Replace the 'puzzle1.txt' with
# any other puzzle file (e.g., 'puzzle2.txt') to play a different game.
PUZZLE_FILE = 'puzzle1.txt'


# Helper functions. 

def get_column(puzzle: str, col_num: int) -> str:
    """Return column col_num of puzzle.

    Precondition: 0 <= col_num < number of columns in puzzle

    >>> get_column('abcd\nefgh\nijkl\n', 1)
    'bfj'
    """

    puzzle_list = puzzle.strip().split('\n')
    column = ''
    for row in puzzle_list:
        column += row[col_num]

    return column


def get_row_length(puzzle: str) -> int:
    """Return the length of a row in puzzle.

    >>> get_row_length('abcd\nefgh\nijkl\n')
    4
    """

    return len(puzzle.split('\n')[0])


def contains(text1: str, text2: str) -> bool:
    """Return whether text2 appears anywhere in text1.

    >>> contains('abc', 'bc')
    True
    >>> contains('abc', 'cb')
    False
    """

    return text2 in text1


def get_current_player(player_one_turn: bool) -> str:
    """Return 'player one' iff player_one_turn is True; otherwise, return
    'player two'.

    >>> get_current_player(True)
    'player one'
    >>> get_current_player(False)
    'player two'
    """
    
    if player_one_turn:
        return P1
    else:
        return P2
    
    
def get_winner(player_one_score: int, player_two_score: int) -> str:
    """Return 'player one wins' iff player_one_score is greater than 
    player_two_score; otherwise, Return 'player two wins' iff player_two_score 
    is greater than player_one_score; otherwise, return 'tie game'.
    
    >>> get_winner(6, 5)
    'player one wins'
    >>> get_winner(6,6)
    'tie game'
    """
    
    if player_one_score > player_two_score:
        return P1_WINS
    elif player_one_score < player_two_score:
        return P2_WINS
    else:
        return TIE


def reverse(line: str) -> str:
    """Return the reverse copy of line.
    
    >>> reverse('zohaib')
    'biahoz'
    >>> reverse('python')
    'nohtyp'
    """ 

    return line[::-1]


def get_row(puzzle: str, row_num: int) -> str:
    """Return row row_num of puzzle.

    Precondition: 0 <= row_num < number of rows in puzzle
    
    >>>get_row('abcd\nefgh\nijkl\n', 2)
    'ijkl'
    >>>get_row('abcde\nfghij\nklmno\n', 1)
    'fghij'
    """
    
    row_length = get_row_length(puzzle)
    first_index = (row_length + 1) * row_num
    last_index = first_index + row_length
    return puzzle[first_index : last_index]


def get_factor(direction: str) -> int:
    """Return the multiplicative factor associated with the direction.
    
       >>>get_factor(UP)
       4   
       >>>get_factor(DOWN)
       2
    """

    if direction == UP:
        return UP_FACTOR
    elif direction == DOWN:
        return DOWN_FACTOR
    elif direction == FORWARD:
        return FORWARD_FACTOR
    else:
        return BACKWARD_FACTOR

    
def get_points(direction: str, words_left: int) -> int:
    """Return the points earned towards the direction when words_left number of 
    words are left.
    
    >>>get_points(BACKWARD, 5)
    15
    >>>get_points(BACKWARD, 1)
    39
    """

    factor = get_factor(direction)
    
    if words_left >= THRESHOLD:
        points = THRESHOLD * factor
    else:
        points = (2 * THRESHOLD - words_left) * factor
        
    if words_left == 1:
        points += BONUS
            
    return points


def check_guess(puzzle: str, direction: str, guessed_word: str, 
                row_or_col_num: int, words_left: int) -> int:
    """Return the number of points earned when a guessed_word in found towards 
    the direction in a row_or_col_num row or column of the puzzle 
    when words_left number of words are left.
    
    Precondition: 0 <= row_or_col_num < number of rows or columns in puzzle 
    
    >>>check_guess('abcd\nefgh\nijkl\n', BACKWARD, 'hgf', 1, 1)
    39
    >>>check_guess('abcd\nefgh\nijkl\n', BACKWARD, 'kji', 2, 5)
    15
    """

    if direction == DOWN and contains(get_column(puzzle, row_or_col_num),
                                      guessed_word):
        return get_points(direction, words_left)
    elif direction == UP and contains(reverse(get_column(puzzle, 
                                                         row_or_col_num)), 
                                      guessed_word):
        return get_points(direction, words_left)
    elif direction == FORWARD and contains(get_row(puzzle, row_or_col_num),
                                           guessed_word):
            return get_points(direction, words_left)
    elif direction == BACKWARD and contains(reverse(get_row(puzzle, 
                                                            row_or_col_num)), 
                                            guessed_word):
            return get_points(direction, words_left)
    else:
        return 0