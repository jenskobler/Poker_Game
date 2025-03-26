# import statements


import numpy as np
import random

import itertools

# constants


CARD_VALUES_STRING = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
CARD_COLORS_STRING = ["hearts", "clubs", "spades", "diamonds"]

HAND_VALUES_STRING = ["high_card", "pair", "two_pair", "three_of_a_kind", "straight", "flush", "full_house", "four_of_a_kind", "straight_flush", "royal_flush"]
HAND_VALUES_STRING.reverse()

# classes


class PokerCard():
    '''
    Poker Card class
    '''
    def __init__(self, value, color):
        self.value = value
        self.color = color
    
    def return_string(self):
        return self.value, self.color


class PokerDeck():
    '''
    Poker Deck class
    '''
    def __init__(self):
        self.cards = []
        
    def generate_complete_deck(self):
        for color in CARD_COLORS_STRING:
            for value in CARD_VALUES_STRING:
                self.cards.append(PokerCard(value,color))

    def draw_random_card(self):
        # compute random position
        random_position = random.randrange(len(self.cards))
        # select and remove card from poker deck
        random_card = self.cards.pop(random_position)
        return random_card
    
    def return_all_cards(self):
        return self.cards


class PokerTable():

    def __init__(self, poker_deck):
        self.states = ["pre-flop", "flop", "turn", "river"]
        self.state = self.states[0]

        self.poker_deck = poker_deck

        self.card_1 = None
        self.card_2 = None
        self.card_3 = None
        self.card_4 = None
        self.card_5 = None

    def next_turn(self):
        
        # to flop
        if self.state == self.states[0]:
            self.card_1 = self.poker_deck.draw_random_card()
            self.card_2 = self.poker_deck.draw_random_card()
            self.card_3 = self.poker_deck.draw_random_card()
            self.state = self.states[1]
        
        # to turn
        elif self.state == self.states[1]:
            self.card_4 = self.poker_deck.draw_random_card()
            self.state = self.states[2]
        
        # to river
        elif self.state == self.states[2]:
            self.card_5 = self.poker_deck.draw_random_card()
            self.state = self.states[3]

    def return_cards(self):
        # flop cards
        if self.state == self.states[1]:
            return [self.card_1, self.card_2, self.card_3]
        # flop + turn cards
        if self.state == self.states[2]:
            return [self.card_1, self.card_2, self.card_3, self.card_4]
        # flop + trun + river cards
        if self.state == self.states[3]:
            return [self.card_1, self.card_2, self.card_3, self.card_4, self.card_5]



# functions



def card_object_2_card_vector(card_object):
    card_vector = np.zeros((len(CARD_COLORS_STRING), len(CARD_VALUES_STRING)))
    color_position = CARD_COLORS_STRING.index(card_object.color)
    value_position = CARD_VALUES_STRING.index(card_object.value)
    card_vector[color_position][value_position] = 1

    return card_vector


def card_vector_2_card_object(card_vector):
    positions = np.where(card_vector == 1)
    value = CARD_VALUES_STRING[int(positions[1][0])]
    color = CARD_COLORS_STRING[int(positions[0][0])]
    card_object = PokerCard(value, color)

    return card_object


def compare_two_cards(card1, card2):
    same_value = False
    same_color = False
    identical = False
    
    if card1.value == card2.value:
        same_value = True
    if card1.color == card2.color:
        same_color = True
    
    if same_value and same_color:
        identical = True
    
    return same_value, same_color, identical
        

def cards_object_list_2_cards_vector_array(cards_object_list):
    cards_vector_list = [card_object_2_card_vector(object) for object in cards_object_list]
    cards_vector_array = np.array(cards_vector_list)
    return cards_vector_array


def cards_vector_array_2_cards_object_list(cards_vector_array):
    cards_object_list = [card_vector_2_card_object(card_vector) for card_vector in cards_vector_array]
    return cards_object_list


## go through each kind of combination


def check_for_pair(cards_vector_array):
    pair_detected = False
    values = []
    for index in range(cards_vector_array.shape[2]):
        sum = cards_vector_array[:,:, index].sum()
        if sum == 2:
            pair_detected = True
            values.append(index)
    return pair_detected, values

def check_for_flush(cards_vector_array):
    flush_detected = False
    for index in range(cards_vector_array.shape[1]):
        sum = cards_vector_array[:, index, :].sum()
        if sum == 5:
            flush_detected = True

    return flush_detected


def check_for_three_of_a_kind(cards_vector_array):
    three_of_a_kind_detected = False
    values = []
    for index in range(cards_vector_array.shape[2]):
        sum = cards_vector_array[:,:, index].sum()
        if sum == 3:
            three_of_a_kind_detected = True
            values.append(index)
    return three_of_a_kind_detected, values

def check_for_four_of_a_kind(cards_vector_array):
    four_of_a_kind_detected = False
    values = []
    for index in range(cards_vector_array.shape[2]):
        sum = cards_vector_array[:,:, index].sum()
        if sum == 4:
            four_of_a_kind_detected = True
            values.append(index)
    return four_of_a_kind_detected, values


def check_for_straight(cards_vector_array):
    straight = False
    kind_of_case = None
    for index_01 in range(9):
        dummy_array = np.zeros(5)
        for index_02 in range(5):
            if cards_vector_array[:,:, index_01+index_02].sum()  > 0 :
                dummy_array[index_02] = 1
        
        sum = dummy_array.sum()
        if sum == 5:
            straight = True
            kind_of_case = index_01

    
    # sonderfall für ass gleich 1
    dummy_array = np.zeros(5)
    for index_02 in range(4):
         if cards_vector_array[:,:, index_02].sum()  > 0 :
            dummy_array[index_02+1] = 1
    if cards_vector_array[:,:, 12].sum()  > 0 :
        dummy_array[0] = 1

    sum = dummy_array.sum()
    if sum == 5:
        straight = True
        kind_of_case = -1
    

    return straight, kind_of_case


def check_for_two_pair(cards_vector_array):
    two_pairs = False
    boolean_value, values = check_for_pair(cards_vector_array)
    if len(values) == 2:
        two_pairs = True

    return two_pairs, values

def check_for_full_house(cards_vector_array):
    full_house = False
    boolean_value_pair, values_pair = check_for_pair(cards_vector_array)
    boolean_value_three, values_three = check_for_three_of_a_kind(cards_vector_array)
    if boolean_value_pair and boolean_value_three:
        full_house = True
    
    return full_house, values_pair, values_three


def check_for_straight_flush(cards_vector_array):
    straight_flush = False
    boolean_straight = check_for_straight(cards_vector_array)[0]
    boolean_flush = check_for_flush(cards_vector_array)

    if boolean_straight and boolean_flush:
        straight_flush = True

    return straight_flush

def check_for_royal_flush(cards_vector_array):
    royal_flush = False
    boolean_straight_flush = check_for_straight_flush(cards_vector_array)
    values = order_card_values(cards_vector_array)

    if values[0] == 12 and values[1] == 11 and boolean_straight_flush:
        royal_flush = True
    return royal_flush

def order_card_values(cards_vector_array):
    '''Funktion um high card einfacher zu bestimmen'''
    cards_object_list = cards_vector_array_2_cards_object_list(cards_vector_array)
    values = []
    for card_object in cards_object_list:
        values.append(CARD_VALUES_STRING.index(card_object.value))

    
    values.sort(reverse=True)

    return values


# def determine_best_hand_of_player(all_seven_cards):
#     pass


    
# more information

class PokerPot():
    def __init__(self):
        self.chips = 0
        self.last_amount_added = None
    
    def add_chips(self, chips):
        self.chips = self.chips + chips
        self.last_amount_added = chips

    def get_pot_size(self):
        return self.chips

    def reset_pot(self):
        self.chips = 0


class PokerPlayer():
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.handcard_1 = None
        self.handcard_2 = None

        self.possible_actions =["raise", "call", "check", "fold"]

        self.is_playing = True
    
    def gets_two_handcards(self, poker_deck):
        self.handcard_1 = poker_deck.draw_random_card()
        self.handcard_2 = poker_deck.draw_random_card()
    
    def add_chips(self, chips):
        self.chips = self.chips + chips

    def subtract_chips(self, chips):
        self.chips = self.chips - chips

    def get_two_handcard_objects(self):
        return [self.handcard_1, self.handcard_2]
    
    def show_handcards(self):
        return (self.handcard_1.value, self.handcard_1.color), (self.handcard_2.value, self.handcard_2.color)

    
    def add_to_pot(self, chips, poker_pot):
        self.subtract_chips(chips)
        poker_pot.add_chips(chips)
        return chips
    
    def input_player_action(self, poker_pot):
        
        player_action = input("Please input your action.")

        if player_action == self.possible_actions[0]:
            chip_amount = input("Please enter amount of chips you want to raise.")
            self.add_to_pot(int(chip_amount), poker_pot)
            print("Player " + str(self.name) + " raises pot with " + str(chip_amount) + " chips.")

        if player_action == self.possible_actions[1]:
            chip_amount = poker_pot.last_amount_added
            self.add_to_pot(int(chip_amount), poker_pot)
            print("Player " + str(self.name) + " calls chip amount " + str(chip_amount) + ".")

        if player_action == self.possible_actions[2]:
            print("Player " + str(self.name) + " checks.")  
        
        if player_action == self.possible_actions[3]:
            self.is_playing = False
            print("Player " + str(self.name) + " folds.")
    
    def get_chip_amount(self):
        return self.chips

    def get_best_poker_hand(self, poker_table):
        all_seven_cards = self.get_two_handcard_objects() + poker_table.return_cards()
        best_hand =  determine_best_hand_of_player(all_seven_cards)
        return best_hand
        

class PokerGame():
    def __init__(self):
        pass

    def initialize_game(self):
        # create PokerDeck
        self.poker_deck = PokerDeck()
        self.poker_deck.generate_complete_deck()
        # check poker deck
        if len(self.poker_deck.return_all_cards()) != 52:
            print("Error!")

        
        # create PokerTable
        self.poker_table = PokerTable(self.poker_deck)

        # create PokerPot
        self.poker_pot = PokerPot()

        # create two players
        self.player_1 = PokerPlayer("Spieler 1", 10)
        self.player_2 = PokerPlayer("Spieler 2", 10)

        # give each player two cards

        self.player_1.gets_two_handcards(self.poker_deck)
        self.player_2.gets_two_handcards(self.poker_deck)

    # Pre-Flop
    def stage_1(self):

        self.get_player_chip_amount()


        print("Show player cards of " + str(self.player_1.name) + "." )
        print(self.player_1.show_handcards())
        self.player_1.input_player_action(self.poker_pot)

        print("Show player cards of " + str(self.player_2.name) + "." )
        print(self.player_2.show_handcards())
        self.player_2.input_player_action(self.poker_pot)

    def check_if_players_are_playing(self):
        if not self.player_1.is_playing:
            print(str(self.player_1.name) + " is not playing anymore.")
        if not self.player_2.is_playing:
            print(str(self.player_2.name) + " is not playing anymore.")

    # Flop
    def stage_2(self):
        self.poker_table.next_turn()

        self.show_table_cards()

        self.get_player_chip_amount()

        self.get_poker_pot_size()


        print("Show player cards of " + str(self.player_1.name) + "." )
        print(self.player_1.show_handcards())
        self.player_1.input_player_action(self.poker_pot)

        print("Show player cards of " + str(self.player_2.name) + "." )
        print(self.player_2.show_handcards())
        self.player_2.input_player_action(self.poker_pot)

    # Turn
    def stage_3(self):
        self.poker_table.next_turn()

        self.show_table_cards()

        self.get_player_chip_amount()

        self.get_poker_pot_size()

        print("Show player cards of " + str(self.player_1.name) + "." )
        print(self.player_1.show_handcards())
        self.player_1.input_player_action(self.poker_pot)

        print("Show player cards of " + str(self.player_2.name) + "." )
        print(self.player_2.show_handcards())
        self.player_2.input_player_action(self.poker_pot)
    
    # River
    def stage_4(self):
        self.poker_table.next_turn()

        self.show_table_cards()

        self.get_player_chip_amount()

        self.get_poker_pot_size()

        print("Show player cards of " + str(self.player_1.name) + "." )
        print(self.player_1.show_handcards())
        self.player_1.input_player_action(self.poker_pot)

        print("Show player cards of " + str(self.player_2.name) + "." )
        print(self.player_2.show_handcards())
        self.player_2.input_player_action(self.poker_pot)


    def show_table_cards(self):
        print("Show table cards")
        table_cards_object_list = self.poker_table.return_cards()
        for card in table_cards_object_list:
            print(card.return_string())
    
    def get_player_chip_amount(self):
        print("Player chip amount")
        print(str(self.player_1.name) + " has the following amount of chips: " + str(self.player_1.get_chip_amount()))
        print(str(self.player_2.name) + " has the following amount of chips: " + str(self.player_1.get_chip_amount()))
    
    def get_poker_pot_size(self):
        print("The pot size is now " + str(self.poker_pot.get_pot_size()) + " chips.")

    def determine_winner(self):
        self.best_hand_of_player_1 = self.player_1.get_best_poker_hand(self.poker_table)
        self.best_hand_of_player_2 = self.player_2.get_best_poker_hand(self.poker_table)
        player_1_won, player_2_won, no_winner = compare_best_hands_of_two_players(self.best_hand_of_player_1, self.best_hand_of_player_2)
        if player_1_won:
            print("Player 1 won.")
        if player_2_won:
            print("Player 2 won.")
        if no_winner:
            print("No one won.")


def get_rough_hand_value(five_cards_object_list):

    cards_vector_array = cards_object_list_2_cards_vector_array(five_cards_object_list)

    # instantiate boolean_dictionary
    boolean_dict = {}
    boolean_dict["high_card"] = True
    boolean_dict["pair"] = False
    boolean_dict["two_pair"] = False
    boolean_dict["three_of_a_kind"] = False
    boolean_dict["straight"] = False
    boolean_dict["flush"] = False
    boolean_dict["full_house"] = False
    boolean_dict["four_of_a_kind"] = False
    boolean_dict["straight_flush"] = False
    boolean_dict["royal_flush"] = False
    boolean_dict["CARD_VECTOR_ARRAY"] = cards_vector_array

    # check for each combination

    boolean_dict["pair"] = check_for_pair(cards_vector_array)[0]
    boolean_dict["two_pair"] = check_for_two_pair(cards_vector_array)[0]
    boolean_dict["three_of_a_kind"] = check_for_three_of_a_kind(cards_vector_array)[0]
    boolean_dict["straight"] = check_for_straight(cards_vector_array)[0]
    boolean_dict["flush"] = check_for_flush(cards_vector_array)
    boolean_dict["full_house"] = check_for_full_house(cards_vector_array)[0]
    boolean_dict["four_of_a_kind"] = check_for_four_of_a_kind(cards_vector_array)[0]
    boolean_dict["straight_flush"] = check_for_straight_flush(cards_vector_array)
    boolean_dict["royal_flush"] = check_for_royal_flush(cards_vector_array)



    return boolean_dict



def decide_based_on_highest_card(highest_card_combinations_list):
    
    # make ordered values 
    original_ordered_values_list = []
    ordered_values_list = []
    for index, combination in enumerate(highest_card_combinations_list):
        original_ordered_values_list.append(order_card_values(combination["CARD_VECTOR_ARRAY"]))
        ordered_values_list.append(order_card_values(combination["CARD_VECTOR_ARRAY"]))

    for i in range(5):
        # search for highest value at specific position
        if len(ordered_values_list) > 1:
            highest_value = 0
            for ordered_values_entry in ordered_values_list:
                value = ordered_values_entry[i]
                if value > highest_value:
                    highest_value = value
            
            # filter list
            updated_highest_card_combinations_list = []
            for ordered_values_entry in ordered_values_list:
                value = ordered_values_entry[i]
                if value == highest_value:
                    updated_highest_card_combinations_list.append(ordered_values_entry)
                

            
            ordered_values_list = updated_highest_card_combinations_list
    

    final_index = original_ordered_values_list.index(ordered_values_list[0])
        

    highest_card_combination = highest_card_combinations_list[final_index]

    

    return highest_card_combination




def check_if_poker_hands_identical(highest_card_combinations_list):
    hand_1 = highest_card_combinations_list[0]
    hand_2 = highest_card_combinations_list[1]

    hand_1_objects = cards_vector_array_2_cards_object_list(hand_1["CARD_VECTOR_ARRAY"])
    hand_2_objects = cards_vector_array_2_cards_object_list(hand_2["CARD_VECTOR_ARRAY"])

    cards_set_1 = set()
    cards_set_2 = set()

    for object in hand_1_objects:
        cards_set_1.add(object.return_string())
    for object in hand_2_objects:
        cards_set_2.add(object.return_string())

    if cards_set_2 == cards_set_1:
        return True
    else:
        return False
    

def compare_best_hands_of_two_players(best_hand_of_player_1, best_hand_of_player_2):
    best_hands = [best_hand_of_player_1, best_hand_of_player_2]
    found_highest_combination = False
    highest_rough_value = None
    for rough_value in HAND_VALUES_STRING:
        # while(not found_highest_combination):
        if not found_highest_combination:
            highest_card_combinations_list = []
            print(rough_value)
            for hand in best_hands:
                if hand[rough_value]:
                    highest_card_combinations_list.append(hand)
                    highest_rough_value = rough_value
        if highest_rough_value != None:
            found_highest_combination = True
            
    
    print(len(highest_card_combinations_list))
    if len(highest_card_combinations_list) == 1:
        best_hand =  highest_card_combinations_list[0]
        if best_hand == best_hands[0]:

            return True, False, False
        if best_hand == best_hands[1]:

            return False, True, False
    # further distinction
    elif len(highest_card_combinations_list) > 1:
        
        # check if identical with set operation and compare two card objects (for example)  
        identical = check_if_poker_hands_identical(highest_card_combinations_list)
        if identical:
            # return "In development"
            return False, False, True
        else:
            # es kann sein, dass hier bei ganz bestimmten sonderfällen falsch bewertet wird ... 
            # (z.B. wenn ein Spieler 2 und 3 hat und der andere auch und auf dem Bort auch eine 2 und eine 3 liegen. 
            # Dann sind die Karten zwar nicht ganz identisch, aber der Wert der Hand ist exakt identisch)
            # nicht ganz sicher, ob es einen error produzieren wird, wahrscheinlich schon -> einfach mal testen und 
            # diesen Sonderfall vorbereiten!
            best_hand = compare_non_identical_hands(highest_card_combinations_list, highest_rough_value)
            if best_hand == best_hands[0]:

                return True, False, False
            if best_hand == best_hands[1]:

                return False, True, False
            
def compare_non_identical_hands(highest_card_combinations_list, highest_rough_value):
    
        
        # compare pair values and then highest card
        if highest_rough_value in ["pair"]:
            # search for highest pair
            highest_pair = 0
            for index, combination in enumerate(highest_card_combinations_list):
                output = check_for_pair(combination["CARD_VECTOR_ARRAY"])
                # print(output)
                if output[1][0] > highest_pair:
                    highest_pair = output[1][0]
            
            # select only combinations with highest three of a kind
            updated_highest_card_combinations_list = []
             
            for index, combination in enumerate(highest_card_combinations_list):
                output = check_for_pair(combination["CARD_VECTOR_ARRAY"])
                if output[1][0] == highest_pair:
                    updated_highest_card_combinations_list.append(combination)

            
            highest_card_combination = decide_based_on_highest_card(updated_highest_card_combinations_list)
            return highest_card_combination
            
        # compare two pair values and then highest card
        if highest_rough_value in ["two_pair"]:
            print("Hello")
            highest_max = 0
            for index, combination in enumerate(highest_card_combinations_list):
                output = check_for_two_pair(combination["CARD_VECTOR_ARRAY"])
                output_max = max(output[1])
                if output_max > highest_max:
                    highest_max = output_max

            # select only combinations with highest max pair
            updated_highest_card_combinations_list = []
             
            for index, combination in enumerate(highest_card_combinations_list):
                output = check_for_two_pair(combination["CARD_VECTOR_ARRAY"])
                output_max = max(output[1])
                if output_max == highest_max:
                    updated_highest_card_combinations_list.append(combination)

            highest_min = 0
            for index, combination in enumerate(updated_highest_card_combinations_list):
                output = check_for_two_pair(combination["CARD_VECTOR_ARRAY"])
                output_min = min(output[1])
                if output_min > highest_min:
                    highest_min = output_min

            # select only combinations with highest min pair
            highest_card_combinations_list = []
             
            for index, combination in enumerate(updated_highest_card_combinations_list):
                output = check_for_two_pair(combination["CARD_VECTOR_ARRAY"])
                output_min = min(output[1])
                if output_min == highest_min:
                    highest_card_combinations_list.append(combination)
            
            highest_card_combination = decide_based_on_highest_card(updated_highest_card_combinations_list)
            return highest_card_combination
            
        # compare full house values 
        if highest_rough_value in ["full_house"]:
            highest_three_of_a_kind = 0
            # search for highest three of a kind
            for index, combination in enumerate(highest_card_combinations_list):
                output = check_for_full_house(combination["CARD_VECTOR_ARRAY"])
                if output[2] > highest_three_of_a_kind:
                    highest_three_of_a_kind = output[2]
            
            # select only combinations with highest three of a kind
            
            updated_highest_card_combinations_list = []
            for index, combination in enumerate(highest_card_combinations_list):
                output = check_for_full_house(combination["CARD_VECTOR_ARRAY"])
                if output[2] == highest_three_of_a_kind:
                    updated_highest_card_combinations_list.append(combination)

            # search for highest pair
            highest_pair = 0
            for index, combination in enumerate(updated_highest_card_combinations_list):
                output = check_for_full_house(combination["CARD_VECTOR_ARRAY"])
                if output[1] > highest_pair:
                    highest_pair = output[1]
            
            # select only combinations with highest three of a kind
            highest_card_combinations_list = []
            for index, combination in enumerate(updated_highest_card_combinations_list):
                output = check_for_full_house(combination["CARD_VECTOR_ARRAY"])
                if output[1] == highest_pair:
                    highest_card_combinations_list.append(combination)
                
            
            return highest_card_combinations_list[0]

                                           
            # if len(values_three) == 1:

            
            

        # compare straight flushs # compare via high card!
        if highest_rough_value in [ "flush", "high_card", "four_of_a_kind"]:
            highest_card_combination = decide_based_on_highest_card(highest_card_combinations_list)
            
            return highest_card_combination

        # need to check special case
        if highest_rough_value in ["straight_flush", "straight"]:
            highest_case = -2
            for index, combination in enumerate(highest_card_combinations_list):
                output = check_for_straight(combination["CARD_VECTOR_ARRAY"])
                if output[1] > highest_case:
                    highest_case = output[1]

            
            updated_highest_card_combinations_list = []
            for index, combination in enumerate(highest_card_combinations_list):
                output= check_for_straight(combination["CARD_VECTOR_ARRAY"])
                if output[1] == highest_case:
                    updated_highest_card_combinations_list.append(combination)

            return updated_highest_card_combinations_list[0]

    # return highest_card_combinations_list[0]


def determine_best_hand_of_player(all_seven_cards):

    all_combinations = []

    # go through each hand combination and determine its rough value
    for index, five_cards_object_list in enumerate(itertools.combinations(all_seven_cards, 5)):
        
        all_combinations.append(get_rough_hand_value(five_cards_object_list))
        # print(index)
        # print(five_cards_object_list)
    
    # select only those combinations with the highest rough value

    # HAND_VALUES_STRING.reverse()
    found_highest_combination = False
    highest_rough_value = None
    for rough_value in HAND_VALUES_STRING:
        # while(not found_highest_combination):
        if not found_highest_combination:
            highest_card_combinations_list = []
            print(rough_value)
            for combination in all_combinations:
                if combination[rough_value]:
                    highest_card_combinations_list.append(combination)
                    highest_rough_value = rough_value
        if highest_rough_value != None:
            found_highest_combination = True
            
    
    print(len(highest_card_combinations_list))
    # TODO
    # compare more in detail:
    if len(highest_card_combinations_list) > 1:
        highest_card_combination = compare_non_identical_hands(highest_card_combinations_list, highest_rough_value)
    
        return highest_card_combination
    elif len(highest_card_combinations_list) == 1:
        
        return highest_card_combinations_list[0]