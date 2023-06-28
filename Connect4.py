
#Modules
from random import randint
from typing import Tuple
from time import sleep

#Constants
BOARD_ROW, BOARD_COL = 6, 7
SEPARATOR = ''.join(['+----'*BOARD_COL]+['+'])

class Connect4:
    """
    Connect4 Class

    The Connect4 class represents a Connect4 game with an AI opponent. It provides functionalities for playing the game, displaying the game board, and keeping track of AI and user statistics.
    """
    
    print('''
    Connect4 Game with AI

    This Connect4 game is designed to showcase advanced techniques for working with nested arrays and includes an AI opponent.

    Features:
        - The AI analyzes possible winning moves based on the player's character symbol to determine the best defensive strategy.
        - The game utilizes nested arrays and algorithms to implement Connect4 logic.
        - The game board is displayed with numbered columns for easy input.
        - Statistics are kept for the AI and user wins.

    Instructions:
        1. Enter your player character ('X' or 'O').
        2. Play by entering a column number to place your token (1-7).
        3. The AI will make its move and display the updated board.
        4. Continue until there is a winner or the game ends.
        5. Play again or quit the game.

    Enjoy the game and challenge the AI with your Connect4 skills!
    ''')
    
    #Stats: [AI, USER]
    stats = [0, 0]
    
    def __init__(self) -> None:
        self.board = [[' ' for _ in range(BOARD_COL)] for _ in range(BOARD_ROW)]
        self.last_move = [-1, -1]
    
    def print_board(self):
        print()
        #Number the columns
        for i in range(1, BOARD_COL+1):
            print(f'  ({i:^1})', end='')
        print()
        print(SEPARATOR)
        for row in range(BOARD_ROW):
            print('|',end='')
            for col in range(BOARD_COL):
                print(f'  {self.board[row][col]:^1} |', end='')
            print()
        print(SEPARATOR)
        print(f'Stats:\n\tAI: {self.stats[0]}\n\tUSER: {self.stats[-1]}'.expandtabs(6))
    
    def set_board(self, col: int, char: str) -> bool:
        '''
        Set the board with a token at the first empty cell of the chosen column.
        
        Args:
            col (int): The column index (1-7) to place the token.
            char (str): The character representing the player's token ('X' or 'O').
            
        Returns:
            bool: True if the token was placed successfully, False otherwise.
        '''
        
        #Checks to see whether col is within the valid range 
        if not 1 <= col <= BOARD_COL:
            return False
        
        #Places each token at the first empty cell of the chosen column
        for row in range(BOARD_ROW - 1, -1, -1):
            if self.board[row][col - 1] == ' ':
                self.board[row][col - 1] = char
                self.last_move = [row, col - 1]
                return True 
        
        return False
    
    def choose_char(self) -> Tuple[str, str]:
        '''
        Function randomly generated character 'X' or 'O'
        Depending on the users choice
        
        Also added a failed counter for fun.
        '''
        count = 0
        CHOICES = ('X', 'O')
        ai_character = lambda user_char: CHOICES[user_char=='X']
        attempts = []
        while (count < 5):
            user_char = input(f'Enter player character {CHOICES}: ').upper()
            attempts.append(user_char)
            if user_char in CHOICES:
                return (user_char, ai_character(user_char))
            elif (user_char not in CHOICES):
                count += 1
                print(f'{user_char} is not an option, only {CHOICES}...   Fail Counter: {count}')
            if count == 5:
                print('\nFailed, your attempted tries:\t')
                print(dict(Attempts=attempts))
    
    def ai(self, ai_char: str, user_char: str) -> None:
        '''
        AI function that first checks possible outcomes by placing
        tokens in each space and checking if it won.
        
        Then will do the same but with the users player character
        do determine whether it should place its token their to
        defend against the user
        
        If AI cant find best column to place token,
        it will place it in any true value
        '''
        
        #Checks to see if the AI wins
        for col in range(1, BOARD_COL + 1):
            if self.set_board(col, ai_char):
                if self.check_win(ai_char):
                    return
                self.board[self.last_move[0]][self.last_move[1]] = ' '
        
        #Checks to see if the user wins
        for col in range(1, BOARD_COL + 1):
            if self.set_board(col, user_char):
                if self.check_win(user_char):
                    self.board[self.last_move[0]][self.last_move[1]] = ' '
                    self.set_board(col, ai_char)
                    return
                self.board[self.last_move[0]][self.last_move[1]] = ' '
        
        #No other options to find
        while True:
            col = randint(1, BOARD_COL)
            if self.set_board(col, ai_char):
                return

    def check_win(self, char: str) -> bool:
        '''
        Functions that returns True if
            1. Any character in a given row contains 4
            2. Any character in a given column contains 4
            2. Any character in a given diagonal contains 4
        '''
        
        # Check rows
        for row in self.board:
            if ''.join(row).count(char * 4) > 0:
                return True
        
        # Check columns
        for col in range(BOARD_COL):
            column = ''.join([self.board[row][col] for row in range(BOARD_ROW)])
            if column.count(char * 4) > 0:
                return True
        
        # Check diagonals
        # Retrieved additional to get the diagonal iteration over enumerating the array to work
        for row, _ in enumerate(self.board[:-3]):
            for col, _ in enumerate(self.board[row][:-3]):
                diagonal1 = ''.join([self.board[row + i][col + i] for i in range(4)])
                if diagonal1.count(char * 4) > 0:
                    return True
                diagonal2 = ''.join([self.board[row + 3 - i][col + i] for i in range(4)])
                if diagonal2.count(char * 4) > 0:
                    return True
        return False

    def player_stats(self, winner):
        '''
        Function to modify and save the player/AI stats if
        game continues to run.
        '''
        
        self.stats[0] += 1 if winner=='AI' else 0
        self.stats[-1] += 1 if winner=='USER' else 0
        


def main() -> None:
    connect4 = Connect4()
    connect4.print_board()
    try: user_char, ai_char = connect4.choose_char()
    except: sleep(0.5); print('\nNo character chosen, ending program.'); raise SystemExit
    RUNNING = True
    try:
        while RUNNING:
            try:
                user_col = int(input('\n(No input == Random value)\nEnter a column to place token (1-7): '))
            except ValueError:
                user_col = randint(1,BOARD_COL)
            while not connect4.set_board(user_col, f'{user_char}'):
                print('Invalid option, try again! ')
                user_col = int(input('\n(No input == Random value)\nEnter a column to place token (1-7): '))
            connect4.print_board()
            connect4.ai(ai_char, user_char)
            sleep(0.2)
            connect4.print_board()
            if (not connect4.check_win(user_char)):
                if connect4.check_win(ai_char):
                    print('\nAI wins!')
                    connect4.player_stats('AI')
                    RUNNING = False
                continue
            else:
                print('Wow, you actually won!')
                connect4.player_stats('USER')
                RUNNING = False
    except KeyboardInterrupt:
        print('\n\nKeyboardInterrupt detected, ending program...')
        print('Good Day!')
        quit()
    connect4.print_board()
    play_again = input('\nPlay again (Y/N)? ')
    if play_again.upper() != 'N':
        main()
    print('Quitting program...')
    sleep(0.5)
    quit()

if __name__ == '__main__':
    main()
