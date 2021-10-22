"""
Link do zasad gry: https://en.wikipedia.org/wiki/Nine_men%27s_morris
Autorzy: Martyna Klebba, Klaudia Pardo
Instrukcja przygotowania środowiska: Potrzebna jest biblioteka "easyAI"

"""
import random
from easyAI import TwoPlayerGame
from easyAI import AI_Player, Negamax

#tablica z przylegającymi punktami
adjacent = [ #poziomo: 0,1,2 #8,9,10 #16,17,18 #3,11,19 #20,12,04 #21,22,23 #13,14,15 #5,6,7
            #pionowo: #0,3,5, #8,11,13 #16,19,21 #1,9,17 #22,14,06 #18,20,23 #10,12,15 #2,4,7
    [1, 3], #0
    [0, 2, 9],#1
    [1, 4],#2
    [0, 5, 11], #3
    [2, 7, 12], #4
    [3, 6], #5
    [5, 7, 14],#6
    [4, 6],#7
    [9, 11],#8
    [1, 8, 10, 17],#9
    [9, 12], #10
    [3, 8, 13, 19],#11
    [4, 10, 15, 20],#12
    [11, 14],#13
    [6, 13, 15, 22], #14
    [12, 14], #15
    [17, 19], #16
    [9, 16, 18], #17
    [17, 20],#18
    [11, 16, 21],#19
    [12, 18, 23],#20
    [19, 22],#21
    [21, 23, 14],#22
    [20, 22] #23
]
# tablica rzędzy i kolumny
mills = [[0, 1, 2], [8, 9, 10], [16, 17, 18], [3, 11, 19], [20, 12, 4], [21, 22, 23], [13, 14, 15],
         [5, 6, 7],  # horiz.
         [0, 3, 5], [8, 11, 13], [16, 19, 21], [1, 9, 17], [22, 14, 6], [18, 20, 23], [10, 12, 15],
         [2, 4, 7]]  # vertical


def printBoard(board): #drukowanie planszy
    print(board[0] + "(00)----------------------" + board[1] +
          "(01)----------------------" + board[2] + "(02)")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|       " + board[8] + "(08)--------------" +
          board[9] + "(09)--------------" + board[10] + "(10)     |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |        " + board[16] + "(16)-----" +
          board[17] + "(17)-----" + board[18] + "(18)       |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print(board[3] + "(03)---" + board[11] + "(11)----" + board[19] + "(19)             " +
          board[20] + "(20)----" + board[12] + "(12)---" + board[4] + "(04)")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |        " + board[21] + "(21)-----" +
          board[22] + "(22)-----" + board[23] + "(23)       |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       " + board[13] + "(13)--------------" +
          board[14] + "(14)--------------" + board[15] + "(15)     |")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|                           |                           |")
    print(board[5] + "(05)----------------------" + board[6] +
          "(06)----------------------" + board[7] + "(07)")
    print("\n")

#klasa pobierająca aktualna pozycje i nastepny ruch
class Move():
    def __init__(self, actual_position, next_move):
        self.actual_position = actual_position
        self.next_move = next_move

    def __str__(self):
        return f"actual_position = {self.actual_position}, next_move = {self.next_move}"


class NineMensMorris(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.board = ['x' for i in range(24)]
        self.nplayer = 1  # player 1 starts.
        self.current_player = 1
        self.actual_stage = 1

    def possible_moves(self):
        """
        Funkcja w przypadku stage'a 1 zwraca tablice z pustymi miejscami gdzie mozna rozstawić pionki
        Kiedy mamy stage 2 albo 3 zwracamy tablice z legalnymi ruchami - czyli gdzie można przesunąć pionki
        :return: lista dozwolonych ruchów
        """
        # stage1 - rozkładanie pionków bez ich przesuwania
        if self.actual_stage == 1:
            empty_fields = []
            #przeszukujemy tablicę, żeby znaleź puste miejsca (puste miejsca oznaczone są 'x')
            blank_fields_found = self.find_elements_on_board('x')
            # przeszukujemy tablice z pozycjami gdzie są puste pola
            for blank_field in blank_fields_found:# dodajemy nowy obiekt do klasy Move() (-1 dlatego, że nie jest wykorzystywany przy rozstawianiu pionków)
                empty_fields.append(Move(-1, blank_field))
            return empty_fields
        # przechodzimy do stage'a 2 i 3
        else:
            found_current_player_pawns = []
            legal_moves = []
            for i in range(24):
                if self.board[i] == str(self.current_player):
                    found_current_player_pawns.append(i)
                    #jesli jednemu z przeciwników zostało mniej niż 3 pionki wchodzimy w stage 3
            if len(found_current_player_pawns) <= 3:
                for i in range(24):
                    if self.board[i] == 'x':
                        for pawn_position in found_current_player_pawns:
                            legal_moves.append(Move(pawn_position, i))

            else: # jesli każdemu z graczy zostało więcej niż 3 pionki zostaje stage 2
                for i in range(24):
                    if self.board[i] == str(self.current_player):
                        for possible_move in adjacent[i]:
                            if self.board[possible_move] == 'x':
                                legal_moves.append(Move(i, possible_move))

            if len(legal_moves) == 0:
                print("No legal moves")

            return legal_moves


    def make_move(self, move):
        """
        Wykona odpowiedni ruch w zależności od stage'a.
        Stage 1: Rozkładamy pionki na planszy
        Stage 2: Przesuwamy pionkami na odpowiednie pola
        Stage 3: Dla gracza któremu zostały 3 pionki - może "skakać" po planszy
        :param move: obiekt move z aktualną i docelową pozycją
        """
        found_pawns = 0
        self.found_pawns_player1 = 0
        self.found_pawns_player2 = 0
        # przeszukujemy tablice do zliczenia ilości pionków każdego z przeciwnikow
        for i in range(24):
            if self.board[i] == '1':
                found_pawns += 1
                self.found_pawns_player1 += 1
            if self.board[i] == '2':
                found_pawns += 1
                self.found_pawns_player2 += 1

        if found_pawns == 17 and self.actual_stage == 1:
            self.actual_stage = 2

        if self.current_player == 1 and self.found_pawns_player1 == 3 and self.actual_stage != 1:
            self.actual_stage = 3
        if self.current_player == 2 and self.found_pawns_player2 == 3 and self.actual_stage != 1:
            self.actual_stage = 3

        if self.actual_stage == 1:
            self.board[move.next_move] = str(self.current_player)
        else:
            #przesuwam pionki albo skacze
            self.board[move.actual_position] = 'x'
            self.board[move.next_move] = f'{str(self.current_player)}'
            found_pawns = self.find_elements_on_board(str(self.current_player))
            """for i in range(24):
                if self.board[i] == str(self.current_player):
                    found_pawns.append(i)"""
            #kiedy gracz ma 3 pionki w rzedzie lub w kolumnie z planszy ściąga pionek przeciwnika
            for mill in mills:
                is_mill = 0
                for pos in mill:
                    for pawn in found_pawns:
                        if pos == pawn:
                            is_mill += 1
                            continue
                if is_mill == 3:
                    found_pawns_opponent = []
                    for i in range(24):
                        if self.board[i] == str(self.opponent_index):
                            found_pawns_opponent.append(i)
                    self.board[random.choice(found_pawns_opponent)] = 'x'

    def lose(self):  # kiedy zostaną 2 pionki
        """
        Przegrana kiedy jednemu z graczy zostały 2 pionki
        :return: Zwraca True kiedy jeden z graczy ma 2 pionki
        """
        # przeszukujemy tablice i zliczamy pionki każdemu z graczy do sprawdzenia czy któryś ma dwa pionki
        found_pawns = 0
        found_pawns_player11 = 0
        found_pawns_player22 = 0
        for i in range(24):
            if self.board[i] == '1':
                found_pawns += 1
                found_pawns_player11 += 1
            if self.board[i] == '2':
                found_pawns += 1
                found_pawns_player22 += 1

        if len(self.possible_moves()) == 0:
            return True

        if self.current_player == 1 and found_pawns_player11 <= 2 and self.actual_stage != 1:
            return True
        elif self.current_player == 2 and found_pawns_player22 <=2 and self.actual_stage != 1:
            return True
        else:
            return False

    def is_over(self): #brak ruchów
        return self.lose()

    def count_elements_on_board(self, *elements):
        """
        Zliczami pionki na planszy
        :param elements: pionki przeciwników '1' albo '2'
        :return: Zwraca liczbe pionkow
        """
        found_elements = 0
        for i in range(24):
            for element in elements:
                if self.board[i] == element:
                    found_elements += 1
        return found_elements

    def find_elements_on_board(self, *elements):
        """
        Szukamy pionków na planszy i dodajemy do tablicy
        :param elements:
        :return: Zwraca tablice ze znaleziony pionkami
        """
        found_elements = []
        for i in range(24):
            for element in elements:
                if self.board[i] == element:
                    found_elements.append(i)
        return found_elements

    def show(self):#printowanie tablicy wyzej
        printBoard(self.board)
        found_pawns = self.count_elements_on_board('1', '2')
        print(f"{found_pawns}")
        print(f"{self.actual_stage}")

    def scoring(self):
        """
        Dodajemy punkty dla gracza któremu udało się ułożyć 3 pionki w rzędzie lub w kolumnie
        :return: Zwraca wynik
        """
        score = 0
        found_pawns = self.find_elements_on_board(str(self.current_player))
        """for i in range(24):
            if self.board[i] == str(self.current_player):
                found_pawns.append(i)"""
        for mill in mills:
            is_mill = 0
            for pos in mill:
                for pawn in found_pawns:
                    if pos == pawn:
                        is_mill += 1
                        continue
            if is_mill == 3:
                score += 20
                #sprawdzić wszystkie pionki przeciwnka
        return score

if __name__ == "__main__":
    ai_algo = Negamax(2)
    #NineMensMorris([AI_Player(ai_algo), AI_Player(ai_algo)]).play(200)
    NineMensMorris([AI_Player, AI_Player(ai_algo)]).play(200)


