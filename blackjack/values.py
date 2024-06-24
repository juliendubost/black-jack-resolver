from enum import Enum


class HandScore(Enum):
    BUST = 0
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15
    SIXTEEN = 16
    SEVENTEEN = 17
    EIGHTEEN = 18
    NINETEEN = 19
    TWENTY = 20
    TWENTY_ONE = 21
    BLACKJACK = 22


class HandState(Enum):
    """
    All possible hand scores for 1 or N cards.
    Represent as well a single card (ex:, bank starting hand) or a hand of multiple cards
     (ex:, player starting hand or player's hand after one card hit)
    Some scores represent a single card, for example ACE is an Ace,
    whereas TEN can be a single card (a ten or a figure) or a combinaison of cards (5 + 5 or 6 + 4)
    Values are used as
     - row and columns index in the transitions arrays
     - abstract score of the hand, used for hands comparison (blackjack = 22 since it is winning against 21)
    """

    BUST = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    FIGURE = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15
    SIXTEEN = 16
    SEVENTEEN = 17
    EIGHTEEN = 18
    NINETEEN = 19
    TWENTY = 20
    ACE = 21
    TWO_TWELVE = 22
    THREE_THIRTEEN = 23
    FOUR_FOURTEEN = 24
    FIVE_FIFTEEN = 25
    SIX_SIXTEEN = 26
    SEVEN_SEVENTEEN = 27
    EIGHT_EIGHTEEN = 28
    NINE_NINETEEN = 29
    TEN_TWENTY = 30
    TWENTY_ONE = 31
    POCKET_ACE = 32
    POCKET_TWO = 33
    POCKET_THREE = 34
    POCKET_FOUR = 35
    POCKET_FIVE = 36
    POCKET_SIX = 37
    POCKET_SEVEN = 38
    POCKET_EIGHT = 39
    POCKET_NINE = 40
    POCKET_FIGURE = 41
    ACE_S = 42  # Special case if you have an ace from a pocket aces split, you are forced to a one card hit without BJ
    BLACKJACK = 43


POCKET_HANDS_TO_STATE = {
    HandState.POCKET_ACE: HandState.ACE_S,
    HandState.POCKET_TWO: HandState.TWO,
    HandState.POCKET_THREE: HandState.THREE,
    HandState.POCKET_FOUR: HandState.FOUR,
    HandState.POCKET_FIVE: HandState.FIVE,
    HandState.POCKET_SIX: HandState.SIX,
    HandState.POCKET_SEVEN: HandState.SEVEN,
    HandState.POCKET_EIGHT: HandState.EIGHT,
    HandState.POCKET_NINE: HandState.NINE,
    HandState.POCKET_FIGURE: HandState.FIGURE,
}

STATE_TO_SCORE = {
    HandState.BUST: HandState.BUST,
    HandState.TWO: HandState.TWO,
    HandState.THREE: HandState.THREE,
    HandState.FOUR: HandState.FOUR,
    HandState.FIVE: HandState.FIVE,
    HandState.SIX: HandState.SIX,
    HandState.SEVEN: HandState.SEVEN,
    HandState.EIGHT: HandState.EIGHT,
    HandState.NINE: HandState.NINE,
    HandState.TEN: HandState.TEN,
    HandState.FIGURE: HandState.TEN,
    HandState.ELEVEN: HandState.ELEVEN,
    HandState.TWELVE: HandState.TWELVE,
    HandState.THIRTEEN: HandState.THIRTEEN,
    HandState.FOURTEEN: HandState.FOURTEEN,
    HandState.FIFTEEN: HandState.FIFTEEN,
    HandState.SIXTEEN: HandState.SIXTEEN,
    HandState.SEVENTEEN: HandState.SEVENTEEN,
    HandState.EIGHTEEN: HandState.EIGHTEEN,
    HandState.NINETEEN: HandState.NINETEEN,
    HandState.TWENTY: HandState.TWENTY,
    HandState.ACE: HandState.ELEVEN,
    HandState.ACE_S: HandState.ELEVEN,
    HandState.TWO_TWELVE: HandState.TWELVE,
    HandState.THREE_THIRTEEN: HandState.THIRTEEN,
    HandState.FOUR_FOURTEEN: HandState.FOURTEEN,
    HandState.FIVE_FIFTEEN: HandState.FIFTEEN,
    HandState.SIX_SIXTEEN: HandState.SIXTEEN,
    HandState.SEVEN_SEVENTEEN: HandState.SEVENTEEN,
    HandState.EIGHT_EIGHTEEN: HandState.EIGHTEEN,
    HandState.NINE_NINETEEN: HandState.NINETEEN,
    HandState.TEN_TWENTY: HandState.TWENTY,
    HandState.TWENTY_ONE: HandState.TWENTY_ONE,
    HandState.POCKET_ACE: HandState.TWELVE,
    HandState.POCKET_TWO: HandState.FOUR,
    HandState.POCKET_THREE: HandState.SIX,
    HandState.POCKET_FOUR: HandState.EIGHT,
    HandState.POCKET_FIVE: HandState.TEN,
    HandState.POCKET_SIX: HandState.TWELVE,
    HandState.POCKET_SEVEN: HandState.FOURTEEN,
    HandState.POCKET_EIGHT: HandState.SIXTEEN,
    HandState.POCKET_NINE: HandState.EIGHTEEN,
    HandState.POCKET_FIGURE: HandState.TWENTY,
    HandState.BLACKJACK: HandState.BLACKJACK,
}

STATE_TO_LABEL = {
    HandState.BUST: "BUST",
    HandState.ACE: "ACE",
    HandState.TWO: "2",
    HandState.THREE: "3",
    HandState.FOUR: "4",
    HandState.FIVE: "5",
    HandState.SIX: "6",
    HandState.SEVEN: "7",
    HandState.EIGHT: "8",
    HandState.NINE: "9",
    HandState.TEN: "10",
    HandState.FIGURE: "10",
    HandState.ELEVEN: "11",
    HandState.TWELVE: "12",
    HandState.THIRTEEN: "13",
    HandState.FOURTEEN: "14",
    HandState.FIFTEEN: "15",
    HandState.SIXTEEN: "16",
    HandState.SEVENTEEN: "17",
    HandState.EIGHTEEN: "18",
    HandState.NINETEEN: "19",
    HandState.TWENTY: "20",
    HandState.TWO_TWELVE: "2-12",
    HandState.THREE_THIRTEEN: "3-13",
    HandState.FOUR_FOURTEEN: "4-14",
    HandState.FIVE_FIFTEEN: "5-15",
    HandState.SIX_SIXTEEN: "6-16",
    HandState.SEVEN_SEVENTEEN: "7-17",
    HandState.EIGHT_EIGHTEEN: "8-18",
    HandState.NINE_NINETEEN: "9-19",
    HandState.TEN_TWENTY: "10-20",
    HandState.TWENTY_ONE: "21",
    HandState.BLACKJACK: "BJ",
}

# All possible hands for the bank to start with
BANK_STARTING_CARDS = [
    HandState.ACE,
    HandState.TWO,
    HandState.THREE,
    HandState.FOUR,
    HandState.FIVE,
    HandState.SIX,
    HandState.SEVEN,
    HandState.EIGHT,
    HandState.NINE,
    HandState.FIGURE,
]

# All hand states for the bank to stand with
BANK_STAND_STATES = [
    HandState.BLACKJACK,
    HandState.BUST,
    HandState.SEVEN_SEVENTEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.NINE_NINETEEN,
    HandState.TEN_TWENTY,
    HandState.SEVENTEEN,
    HandState.EIGHTEEN,
    HandState.NINETEEN,
    HandState.TWENTY,
    HandState.TWENTY_ONE,
]

# All hand scores for the bank to stand with
BANK_STAND_SCORES = [
    HandState.SEVENTEEN,
    HandState.EIGHTEEN,
    HandState.NINETEEN,
    HandState.TWENTY,
    HandState.TWENTY_ONE,
    HandState.BLACKJACK,
    HandState.BUST,
]

# All possible hands for the player to start with
PLAYER_STARTING_STATES = [
    HandState.BLACKJACK,
    HandState.TWO,
    HandState.THREE,
    HandState.FOUR,
    HandState.FIVE,
    HandState.SIX,
    HandState.SEVEN,
    HandState.EIGHT,
    HandState.NINE,
    HandState.TEN,
    HandState.ELEVEN,
    HandState.TWELVE,
    HandState.THIRTEEN,
    HandState.FOURTEEN,
    HandState.FIFTEEN,
    HandState.SIXTEEN,
    HandState.SEVENTEEN,
    HandState.EIGHTEEN,
    HandState.NINETEEN,
    HandState.TWENTY,
    HandState.THREE_THIRTEEN,
    HandState.FOUR_FOURTEEN,
    HandState.FIVE_FIFTEEN,
    HandState.SIX_SIXTEEN,
    HandState.SEVEN_SEVENTEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.NINE_NINETEEN,
    HandState.TEN_TWENTY,
    HandState.POCKET_ACE,
    HandState.POCKET_TWO,
    HandState.POCKET_THREE,
    HandState.POCKET_FOUR,
    HandState.POCKET_FIVE,
    HandState.POCKET_SIX,
    HandState.POCKET_SEVEN,
    HandState.POCKET_EIGHT,
    HandState.POCKET_NINE,
    HandState.POCKET_FIGURE,
]

# All suitable hand scores for the player to stand with
PLAYER_STAND_STATES = [
    HandState.BLACKJACK,
    HandState.THREE_THIRTEEN,
    HandState.FOUR_FOURTEEN,
    HandState.FIVE_FIFTEEN,
    HandState.SIX_SIXTEEN,
    HandState.SEVEN_SEVENTEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.NINE_NINETEEN,
    HandState.TEN_TWENTY,
    HandState.TWELVE,
    HandState.THIRTEEN,
    HandState.FOURTEEN,
    HandState.FIFTEEN,
    HandState.SIXTEEN,
    HandState.SEVENTEEN,
    HandState.EIGHTEEN,
    HandState.NINETEEN,
    HandState.TWENTY,
    HandState.TWENTY_ONE,
]

# All states on which player is forced to stand
PLAYER_END_STATES = [
    HandState.BLACKJACK,
    HandState.BUST,
    HandState.TWENTY_ONE,
]

# All possible hand scores after a card hit
POST_HIT_CARDS = [
    HandState.BLACKJACK,
    HandState.TWO_TWELVE,
    HandState.THREE_THIRTEEN,
    HandState.FOUR_FOURTEEN,
    HandState.FIVE_FIFTEEN,
    HandState.SIX_SIXTEEN,
    HandState.SEVEN_SEVENTEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.NINE_NINETEEN,
    HandState.TEN_TWENTY,
    HandState.TWELVE,
    HandState.THIRTEEN,
    HandState.FOURTEEN,
    HandState.FIFTEEN,
    HandState.SIXTEEN,
    HandState.SEVENTEEN,
    HandState.EIGHTEEN,
    HandState.NINETEEN,
    HandState.TWENTY,
    HandState.TWENTY_ONE,
]

# All relevant hand scores before a hit.
# In this case we do not consider pocket hands, blackjack or 21 since it's no more relevant
PRE_HIT_CARDS = [
    HandState.ACE,
    HandState.ACE_S,
    HandState.TWO,
    HandState.THREE,
    HandState.FOUR,
    HandState.FIVE,
    HandState.SIX,
    HandState.SEVEN,
    HandState.EIGHT,
    HandState.NINE,
    HandState.TEN,
    HandState.FIGURE,
    HandState.ELEVEN,
    HandState.TWELVE,
    HandState.THIRTEEN,
    HandState.FOURTEEN,
    HandState.FIFTEEN,
    HandState.SIXTEEN,
    HandState.SEVENTEEN,
    HandState.EIGHTEEN,
    HandState.NINETEEN,
    HandState.TWENTY,
    HandState.TWO_TWELVE,
    HandState.THREE_THIRTEEN,
    HandState.FOUR_FOURTEEN,
    HandState.FIVE_FIFTEEN,
    HandState.SIX_SIXTEEN,
    HandState.SEVEN_SEVENTEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.NINE_NINETEEN,
    HandState.TEN_TWENTY,
    HandState.POCKET_ACE,
    HandState.POCKET_TWO,
    HandState.POCKET_THREE,
    HandState.POCKET_FOUR,
    HandState.POCKET_FIVE,
    HandState.POCKET_SIX,
    HandState.POCKET_SEVEN,
    HandState.POCKET_EIGHT,
    HandState.POCKET_NINE,
    HandState.POCKET_FIGURE,
]

# All possible hit cards
HIT_CARDS = [
    HandState.ACE,
    HandState.TWO,
    HandState.THREE,
    HandState.FOUR,
    HandState.FIVE,
    HandState.SIX,
    HandState.SEVEN,
    HandState.EIGHT,
    HandState.NINE,
    HandState.FIGURE,
]
