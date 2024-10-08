from enum import Enum
from blackjack import settings


class HandState(Enum):
    """
    All possible hand scores for 1 or N cards.
    Represent as well a single card (ex:, bank starting hand) or a hand of multiple cards
     (ex:, player starting hand or player's hand after one card hit)
    Some scores represent a single card, for example ACE is an Ace,
    whereas TEN can be a single card (a ten or a figure) or a combination of cards (5 + 5 or 6 + 4)
    Values are used as
     - row and columns index in the transitions arrays
     - abstract integer for the hand, this integer is relative to the force of the hand
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
    BLACKJACK = 42

    def __str__(self):
        return STATE_TO_LABEL[self]


POCKET_HANDS_TO_STATE = {
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

# Point value of each card, used to determine the 2-cards hand state
STATE_TO_POINTS = {
    HandState.TWO: 2,
    HandState.THREE: 3,
    HandState.FOUR: 4,
    HandState.FIVE: 5,
    HandState.SIX: 6,
    HandState.SEVEN: 7,
    HandState.EIGHT: 8,
    HandState.NINE: 9,
    HandState.FIGURE: 10,
    HandState.ACE: 11,
}

# Give your starting state with 2 not-aces & not-equals cards knowing the hand points
POINTS_TO_HARD_STATE = {
    5: HandState.FIVE,
    6: HandState.SIX,
    7: HandState.SEVEN,
    8: HandState.EIGHT,
    9: HandState.NINE,
    10: HandState.TEN,
    11: HandState.ELEVEN,
    12: HandState.TWELVE,
    13: HandState.THIRTEEN,
    14: HandState.FOURTEEN,
    15: HandState.FIFTEEN,
    16: HandState.SIXTEEN,
    17: HandState.SEVENTEEN,
    18: HandState.EIGHTEEN,
    19: HandState.NINETEEN,
    20: HandState.TWENTY,
}

# Give your starting state with 2 not-equals cards where at least one card is an ace knowing the hand points
POINTS_TO_SOFT_STATE = {
    13: HandState.THREE_THIRTEEN,
    14: HandState.FOUR_FOURTEEN,
    15: HandState.FIVE_FIFTEEN,
    16: HandState.SIX_SIXTEEN,
    17: HandState.SEVEN_SEVENTEEN,
    18: HandState.EIGHT_EIGHTEEN,
    19: HandState.NINE_NINETEEN,
    20: HandState.TEN_TWENTY,
    21: HandState.BLACKJACK,  # Because it contains an ace, this specific case is put in soft states
}

# Give your starting state with 2 equals cards knowing the hand points
POINTS_TO_POCKET_STATE = {
    22: HandState.POCKET_ACE,
    4: HandState.POCKET_TWO,
    6: HandState.POCKET_THREE,
    8: HandState.POCKET_FOUR,
    10: HandState.POCKET_FIVE,
    12: HandState.POCKET_SIX,
    14: HandState.POCKET_SEVEN,
    16: HandState.POCKET_EIGHT,
    18: HandState.POCKET_NINE,
    20: HandState.POCKET_FIGURE,
}


STATE_TO_LABEL = {
    HandState.BUST: "BUST",
    HandState.ACE: "A",
    HandState.TWO: "2",
    HandState.THREE: "3",
    HandState.FOUR: "4",
    HandState.FIVE: "5",
    HandState.SIX: "6",
    HandState.SEVEN: "7",
    HandState.EIGHT: "8",
    HandState.NINE: "9",
    HandState.TEN: "10",
    HandState.FIGURE: "F",
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
    HandState.POCKET_ACE: "1-1",
    HandState.POCKET_TWO: "2-2",
    HandState.POCKET_THREE: "3-3",
    HandState.POCKET_FOUR: "4-4",
    HandState.POCKET_FIVE: "5-5",
    HandState.POCKET_SIX: "6-6",
    HandState.POCKET_SEVEN: "7-7",
    HandState.POCKET_EIGHT: "8-8",
    HandState.POCKET_NINE: "9-9",
    HandState.POCKET_FIGURE: "10-10",
}

# All possible hands for the bank to start with
BANK_STARTING_CARDS = [
    HandState.TWO,
    HandState.THREE,
    HandState.FOUR,
    HandState.FIVE,
    HandState.SIX,
    HandState.SEVEN,
    HandState.EIGHT,
    HandState.NINE,
    HandState.FIGURE,
    HandState.ACE,
]

# All hand states for the bank to stand with
BANK_STAND_STATES = [
    HandState.BLACKJACK,
    HandState.BUST,
    HandState.EIGHT_EIGHTEEN,
    HandState.NINE_NINETEEN,
    HandState.TEN_TWENTY,
    HandState.SEVENTEEN,
    HandState.EIGHTEEN,
    HandState.NINETEEN,
    HandState.TWENTY,
    HandState.TWENTY_ONE,
]
if not settings.DEALER_HIT_ON_SOFT_17:
    # This state is added only if dealer does not hit on a soft 17
    BANK_STAND_STATES.append(HandState.SEVEN_SEVENTEEN)


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

# All possible states a player can face during the game
PLAYER_POSSIBLE_STATES = [
    HandState.BLACKJACK,
    HandState.TWENTY,
    HandState.NINETEEN,
    HandState.EIGHTEEN,
    HandState.SEVENTEEN,
    HandState.SIXTEEN,
    HandState.FIFTEEN,
    HandState.FOURTEEN,
    HandState.THIRTEEN,
    HandState.TWENTY_ONE,
    HandState.TWELVE,
    HandState.ELEVEN,
    HandState.TEN,
    HandState.NINE,
    HandState.EIGHT,
    HandState.SEVEN,
    HandState.SIX,
    HandState.FIVE,
    HandState.FOUR,
    HandState.TEN_TWENTY,
    HandState.NINE_NINETEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.SEVEN_SEVENTEEN,
    HandState.SIX_SIXTEEN,
    HandState.FIVE_FIFTEEN,
    HandState.FOUR_FOURTEEN,
    HandState.THREE_THIRTEEN,
    HandState.TWO_TWELVE,
    HandState.POCKET_ACE,
    HandState.POCKET_FIGURE,
    HandState.POCKET_NINE,
    HandState.POCKET_EIGHT,
    HandState.POCKET_SEVEN,
    HandState.POCKET_SIX,
    HandState.POCKET_FIVE,
    HandState.POCKET_FOUR,
    HandState.POCKET_THREE,
    HandState.POCKET_TWO,
]

# All hard states for a player
PLAYER_HARD_STATES = [
    HandState.TWENTY,
    HandState.NINETEEN,
    HandState.EIGHTEEN,
    HandState.SEVENTEEN,
    HandState.SIXTEEN,
    HandState.FIFTEEN,
    HandState.FOURTEEN,
    HandState.THIRTEEN,
    HandState.TWELVE,
    HandState.ELEVEN,
    HandState.TEN,
    HandState.NINE,
    HandState.EIGHT,
    HandState.SEVEN,
    HandState.SIX,
    HandState.FIVE,
    HandState.FOUR,
]

# All soft states for a player
PLAYER_SOFT_STATES = [
    HandState.TEN_TWENTY,
    HandState.NINE_NINETEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.SEVEN_SEVENTEEN,
    HandState.SIX_SIXTEEN,
    HandState.FIVE_FIFTEEN,
    HandState.FOUR_FOURTEEN,
    HandState.THREE_THIRTEEN,
    HandState.TWO_TWELVE,
]

# All player pocket pairs state
PLAYER_PAIRS_STATES = [
    HandState.POCKET_ACE,
    HandState.POCKET_FIGURE,
    HandState.POCKET_NINE,
    HandState.POCKET_EIGHT,
    HandState.POCKET_SEVEN,
    HandState.POCKET_SIX,
    HandState.POCKET_FIVE,
    HandState.POCKET_FOUR,
    HandState.POCKET_THREE,
    HandState.POCKET_TWO,
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

# Given hand value (key of TRANSITIONS dict) and car value (key of the subdict),
# value is the result obtained after a hit (or double) action
# no value = hand is burned
HIT_TRANSITIONS = {
    # Figure is used to represent a single 10 or figure card
    # Ten is used to represent a ten score with 2 or more cards (6+4 or 5+5 or 7+3)
    # This is to distinguish the blackjack case: you can transition to blackjack with a single ten
    # but not with a 2-cards 10 score
    HandState.BUST: {},
    HandState.TWO: {
        HandState.ACE: HandState.THREE_THIRTEEN,
        HandState.TWO: HandState.FOUR,
        HandState.THREE: HandState.FIVE,
        HandState.FOUR: HandState.SIX,
        HandState.FIVE: HandState.SEVEN,
        HandState.SIX: HandState.EIGHT,
        HandState.SEVEN: HandState.NINE,
        HandState.EIGHT: HandState.TEN,
        HandState.NINE: HandState.ELEVEN,
        HandState.FIGURE: HandState.TWELVE,
    },
    HandState.THREE: {
        HandState.ACE: HandState.FOUR_FOURTEEN,
        HandState.TWO: HandState.FIVE,
        HandState.THREE: HandState.SIX,
        HandState.FOUR: HandState.SEVEN,
        HandState.FIVE: HandState.EIGHT,
        HandState.SIX: HandState.NINE,
        HandState.SEVEN: HandState.TEN,
        HandState.EIGHT: HandState.ELEVEN,
        HandState.NINE: HandState.TWELVE,
        HandState.FIGURE: HandState.THIRTEEN,
    },
    HandState.FOUR: {
        HandState.ACE: HandState.FIVE_FIFTEEN,
        HandState.TWO: HandState.SIX,
        HandState.THREE: HandState.SEVEN,
        HandState.FOUR: HandState.EIGHT,
        HandState.FIVE: HandState.NINE,
        HandState.SIX: HandState.TEN,
        HandState.SEVEN: HandState.ELEVEN,
        HandState.EIGHT: HandState.TWELVE,
        HandState.NINE: HandState.THIRTEEN,
        HandState.FIGURE: HandState.FOURTEEN,
    },
    HandState.FIVE: {
        HandState.ACE: HandState.SIX_SIXTEEN,
        HandState.TWO: HandState.SEVEN,
        HandState.THREE: HandState.EIGHT,
        HandState.FOUR: HandState.NINE,
        HandState.FIVE: HandState.TEN,
        HandState.SIX: HandState.ELEVEN,
        HandState.SEVEN: HandState.TWELVE,
        HandState.EIGHT: HandState.THIRTEEN,
        HandState.NINE: HandState.THIRTEEN,
        HandState.FIGURE: HandState.FIFTEEN,
    },
    HandState.SIX: {
        HandState.ACE: HandState.SEVEN_SEVENTEEN,
        HandState.TWO: HandState.EIGHT,
        HandState.THREE: HandState.NINE,
        HandState.FOUR: HandState.TEN,
        HandState.FIVE: HandState.ELEVEN,
        HandState.SIX: HandState.TWELVE,
        HandState.SEVEN: HandState.THIRTEEN,
        HandState.EIGHT: HandState.FOURTEEN,
        HandState.NINE: HandState.FIFTEEN,
        HandState.FIGURE: HandState.SIXTEEN,
    },
    HandState.SEVEN: {
        HandState.ACE: HandState.EIGHT_EIGHTEEN,
        HandState.TWO: HandState.NINE,
        HandState.THREE: HandState.TEN,
        HandState.FOUR: HandState.ELEVEN,
        HandState.FIVE: HandState.TWELVE,
        HandState.SIX: HandState.THIRTEEN,
        HandState.SEVEN: HandState.FOURTEEN,
        HandState.EIGHT: HandState.FIFTEEN,
        HandState.NINE: HandState.SIXTEEN,
        HandState.FIGURE: HandState.SEVENTEEN,
    },
    HandState.EIGHT: {
        HandState.ACE: HandState.NINE_NINETEEN,
        HandState.TWO: HandState.TEN,
        HandState.THREE: HandState.ELEVEN,
        HandState.FOUR: HandState.TWELVE,
        HandState.FIVE: HandState.THIRTEEN,
        HandState.SIX: HandState.FOURTEEN,
        HandState.SEVEN: HandState.FIFTEEN,
        HandState.EIGHT: HandState.SIXTEEN,
        HandState.NINE: HandState.SEVENTEEN,
        HandState.FIGURE: HandState.EIGHTEEN,
    },
    HandState.NINE: {
        HandState.ACE: HandState.TEN_TWENTY,
        HandState.TWO: HandState.ELEVEN,
        HandState.THREE: HandState.TWELVE,
        HandState.FOUR: HandState.THIRTEEN,
        HandState.FIVE: HandState.FOURTEEN,
        HandState.SIX: HandState.FIFTEEN,
        HandState.SEVEN: HandState.SIXTEEN,
        HandState.EIGHT: HandState.SEVENTEEN,
        HandState.NINE: HandState.EIGHTEEN,
        HandState.FIGURE: HandState.NINETEEN,
    },
    HandState.TEN: {
        HandState.ACE: HandState.TWENTY_ONE,
        HandState.TWO: HandState.TWELVE,
        HandState.THREE: HandState.THIRTEEN,
        HandState.FOUR: HandState.FOURTEEN,
        HandState.FIVE: HandState.FIFTEEN,
        HandState.SIX: HandState.SIXTEEN,
        HandState.SEVEN: HandState.SEVENTEEN,
        HandState.EIGHT: HandState.EIGHTEEN,
        HandState.NINE: HandState.NINETEEN,
        HandState.FIGURE: HandState.TWENTY,
    },
    HandState.FIGURE: {
        HandState.ACE: HandState.BLACKJACK,
        HandState.TWO: HandState.TWELVE,
        HandState.THREE: HandState.THIRTEEN,
        HandState.FOUR: HandState.FOURTEEN,
        HandState.FIVE: HandState.FIFTEEN,
        HandState.SIX: HandState.SIXTEEN,
        HandState.SEVEN: HandState.SEVENTEEN,
        HandState.EIGHT: HandState.EIGHTEEN,
        HandState.NINE: HandState.NINETEEN,
        HandState.FIGURE: HandState.TWENTY,
    },
    HandState.ELEVEN: {
        HandState.ACE: HandState.TWELVE,
        HandState.TWO: HandState.THIRTEEN,
        HandState.THREE: HandState.FOURTEEN,
        HandState.FOUR: HandState.FIFTEEN,
        HandState.FIVE: HandState.SIXTEEN,
        HandState.SIX: HandState.SEVENTEEN,
        HandState.SEVEN: HandState.EIGHTEEN,
        HandState.EIGHT: HandState.NINETEEN,
        HandState.NINE: HandState.TWENTY,
        HandState.FIGURE: HandState.TWENTY_ONE,
    },
    HandState.TWELVE: {
        HandState.ACE: HandState.THIRTEEN,
        HandState.TWO: HandState.FOURTEEN,
        HandState.THREE: HandState.FIFTEEN,
        HandState.FOUR: HandState.SIXTEEN,
        HandState.FIVE: HandState.SEVENTEEN,
        HandState.SIX: HandState.EIGHTEEN,
        HandState.SEVEN: HandState.NINETEEN,
        HandState.EIGHT: HandState.TWENTY,
        HandState.NINE: HandState.TWENTY_ONE,
    },
    HandState.THIRTEEN: {
        HandState.ACE: HandState.FOURTEEN,
        HandState.TWO: HandState.FIFTEEN,
        HandState.THREE: HandState.SIXTEEN,
        HandState.FOUR: HandState.SEVENTEEN,
        HandState.FIVE: HandState.EIGHTEEN,
        HandState.SIX: HandState.NINETEEN,
        HandState.SEVEN: HandState.TWENTY,
        HandState.EIGHT: HandState.TWENTY_ONE,
    },
    HandState.FOURTEEN: {
        HandState.ACE: HandState.FIFTEEN,
        HandState.TWO: HandState.SIXTEEN,
        HandState.THREE: HandState.SEVENTEEN,
        HandState.FOUR: HandState.EIGHTEEN,
        HandState.FIVE: HandState.NINETEEN,
        HandState.SIX: HandState.TWENTY,
        HandState.SEVEN: HandState.TWENTY_ONE,
    },
    HandState.FIFTEEN: {
        HandState.ACE: HandState.SIXTEEN,
        HandState.TWO: HandState.SEVENTEEN,
        HandState.THREE: HandState.EIGHTEEN,
        HandState.FOUR: HandState.NINETEEN,
        HandState.FIVE: HandState.TWENTY,
        HandState.SIX: HandState.TWENTY_ONE,
    },
    HandState.SIXTEEN: {
        HandState.ACE: HandState.SEVENTEEN,
        HandState.TWO: HandState.EIGHTEEN,
        HandState.THREE: HandState.NINETEEN,
        HandState.FOUR: HandState.TWENTY,
        HandState.FIVE: HandState.TWENTY_ONE,
    },
    HandState.SEVENTEEN: {
        HandState.ACE: HandState.EIGHTEEN,
        HandState.TWO: HandState.NINETEEN,
        HandState.THREE: HandState.TWENTY,
        HandState.FOUR: HandState.TWENTY_ONE,
    },
    HandState.EIGHTEEN: {
        HandState.ACE: HandState.NINETEEN,
        HandState.TWO: HandState.TWENTY,
        HandState.THREE: HandState.TWENTY_ONE,
    },
    HandState.NINETEEN: {
        HandState.ACE: HandState.TWENTY,
        HandState.TWO: HandState.TWENTY_ONE,
    },
    HandState.TWENTY: {
        HandState.ACE: HandState.TWENTY_ONE,
    },
    # Soft hands
    HandState.ACE: {
        HandState.ACE: HandState.TWO_TWELVE,
        HandState.TWO: HandState.THREE_THIRTEEN,
        HandState.THREE: HandState.FOUR_FOURTEEN,
        HandState.FOUR: HandState.FIVE_FIFTEEN,
        HandState.FIVE: HandState.SIX_SIXTEEN,
        HandState.SIX: HandState.SEVEN_SEVENTEEN,
        HandState.SEVEN: HandState.EIGHT_EIGHTEEN,
        HandState.EIGHT: HandState.NINE_NINETEEN,
        HandState.NINE: HandState.TEN_TWENTY,
        HandState.FIGURE: HandState.BLACKJACK,
    },
    HandState.TWO_TWELVE: {
        HandState.ACE: HandState.THREE_THIRTEEN,
        HandState.TWO: HandState.FOUR_FOURTEEN,
        HandState.THREE: HandState.FIVE_FIFTEEN,
        HandState.FOUR: HandState.SIX_SIXTEEN,
        HandState.FIVE: HandState.SEVEN_SEVENTEEN,
        HandState.SIX: HandState.EIGHT_EIGHTEEN,
        HandState.SEVEN: HandState.NINE_NINETEEN,
        HandState.EIGHT: HandState.TEN_TWENTY,
        HandState.NINE: HandState.TWENTY_ONE,
        HandState.FIGURE: HandState.TWELVE,
    },
    HandState.THREE_THIRTEEN: {
        HandState.ACE: HandState.FOUR_FOURTEEN,
        HandState.TWO: HandState.FIVE_FIFTEEN,
        HandState.THREE: HandState.SIX_SIXTEEN,
        HandState.FOUR: HandState.SEVEN_SEVENTEEN,
        HandState.FIVE: HandState.EIGHT_EIGHTEEN,
        HandState.SIX: HandState.NINE_NINETEEN,
        HandState.SEVEN: HandState.TEN_TWENTY,
        HandState.EIGHT: HandState.TWENTY_ONE,
        HandState.NINE: HandState.TWELVE,
        HandState.FIGURE: HandState.THIRTEEN,
    },
    HandState.FOUR_FOURTEEN: {
        HandState.ACE: HandState.FIVE_FIFTEEN,
        HandState.TWO: HandState.SIX_SIXTEEN,
        HandState.THREE: HandState.SEVEN_SEVENTEEN,
        HandState.FOUR: HandState.EIGHT_EIGHTEEN,
        HandState.FIVE: HandState.NINE_NINETEEN,
        HandState.SIX: HandState.TEN_TWENTY,
        HandState.SEVEN: HandState.TWENTY_ONE,
        HandState.EIGHT: HandState.TWELVE,
        HandState.NINE: HandState.THIRTEEN,
        HandState.FIGURE: HandState.FOURTEEN,
    },
    HandState.FIVE_FIFTEEN: {
        HandState.ACE: HandState.SIX_SIXTEEN,
        HandState.TWO: HandState.SEVEN_SEVENTEEN,
        HandState.THREE: HandState.EIGHT_EIGHTEEN,
        HandState.FOUR: HandState.NINE_NINETEEN,
        HandState.FIVE: HandState.TEN_TWENTY,
        HandState.SIX: HandState.TWENTY_ONE,
        HandState.SEVEN: HandState.TWELVE,
        HandState.EIGHT: HandState.THIRTEEN,
        HandState.NINE: HandState.FOURTEEN,
        HandState.FIGURE: HandState.FIFTEEN,
    },
    HandState.SIX_SIXTEEN: {
        HandState.ACE: HandState.SEVEN_SEVENTEEN,
        HandState.TWO: HandState.EIGHT_EIGHTEEN,
        HandState.THREE: HandState.NINE_NINETEEN,
        HandState.FOUR: HandState.TEN_TWENTY,
        HandState.FIVE: HandState.TWENTY_ONE,
        HandState.SIX: HandState.TWELVE,
        HandState.SEVEN: HandState.THIRTEEN,
        HandState.EIGHT: HandState.FOURTEEN,
        HandState.NINE: HandState.FIFTEEN,
        HandState.FIGURE: HandState.SIXTEEN,
    },
    HandState.SEVEN_SEVENTEEN: {
        HandState.ACE: HandState.EIGHT_EIGHTEEN,
        HandState.TWO: HandState.NINE_NINETEEN,
        HandState.THREE: HandState.TEN_TWENTY,
        HandState.FOUR: HandState.TWENTY_ONE,
        HandState.FIVE: HandState.TWELVE,
        HandState.SIX: HandState.THIRTEEN,
        HandState.SEVEN: HandState.FOURTEEN,
        HandState.EIGHT: HandState.FIFTEEN,
        HandState.NINE: HandState.SIXTEEN,
        HandState.FIGURE: HandState.SEVENTEEN,
    },
    HandState.EIGHT_EIGHTEEN: {
        HandState.ACE: HandState.NINE_NINETEEN,
        HandState.TWO: HandState.TEN_TWENTY,
        HandState.THREE: HandState.TWENTY_ONE,
        HandState.FOUR: HandState.TWELVE,
        HandState.FIVE: HandState.THIRTEEN,
        HandState.SIX: HandState.FOURTEEN,
        HandState.SEVEN: HandState.FIFTEEN,
        HandState.EIGHT: HandState.SIXTEEN,
        HandState.NINE: HandState.SEVENTEEN,
        HandState.FIGURE: HandState.EIGHTEEN,
    },
    HandState.NINE_NINETEEN: {
        HandState.ACE: HandState.TEN_TWENTY,
        HandState.TWO: HandState.TWENTY_ONE,
        HandState.THREE: HandState.TWELVE,
        HandState.FOUR: HandState.THIRTEEN,
        HandState.FIVE: HandState.FOURTEEN,
        HandState.SIX: HandState.FIFTEEN,
        HandState.SEVEN: HandState.SIXTEEN,
        HandState.EIGHT: HandState.SEVENTEEN,
        HandState.NINE: HandState.EIGHTEEN,
        HandState.FIGURE: HandState.NINETEEN,
    },
    HandState.TEN_TWENTY: {
        HandState.ACE: HandState.TWENTY_ONE,
        HandState.TWO: HandState.TWELVE,
        HandState.THREE: HandState.THIRTEEN,
        HandState.FOUR: HandState.FOURTEEN,
        HandState.FIVE: HandState.FIFTEEN,
        HandState.SIX: HandState.SIXTEEN,
        HandState.SEVEN: HandState.SEVENTEEN,
        HandState.EIGHT: HandState.EIGHTEEN,
        HandState.NINE: HandState.NINETEEN,
        HandState.FIGURE: HandState.TWENTY,
    },
}
# Add pocket hands transitions
HIT_TRANSITIONS[HandState.POCKET_ACE] = HIT_TRANSITIONS[HandState.TWO_TWELVE]
HIT_TRANSITIONS[HandState.POCKET_TWO] = HIT_TRANSITIONS[HandState.FOUR]
HIT_TRANSITIONS[HandState.POCKET_THREE] = HIT_TRANSITIONS[HandState.SIX]
HIT_TRANSITIONS[HandState.POCKET_FOUR] = HIT_TRANSITIONS[HandState.EIGHT]
HIT_TRANSITIONS[HandState.POCKET_FIVE] = HIT_TRANSITIONS[HandState.TEN]
HIT_TRANSITIONS[HandState.POCKET_SIX] = HIT_TRANSITIONS[HandState.TWELVE]
HIT_TRANSITIONS[HandState.POCKET_SEVEN] = HIT_TRANSITIONS[HandState.FOURTEEN]
HIT_TRANSITIONS[HandState.POCKET_EIGHT] = HIT_TRANSITIONS[HandState.SIXTEEN]
HIT_TRANSITIONS[HandState.POCKET_NINE] = HIT_TRANSITIONS[HandState.EIGHTEEN]
HIT_TRANSITIONS[HandState.POCKET_FIGURE] = HIT_TRANSITIONS[HandState.TWENTY]

HIT_PROBABILITIES = {
    HandState.ACE: 1 / 13,
    HandState.TWO: 1 / 13,
    HandState.THREE: 1 / 13,
    HandState.FOUR: 1 / 13,
    HandState.FIVE: 1 / 13,
    HandState.SIX: 1 / 13,
    HandState.SEVEN: 1 / 13,
    HandState.EIGHT: 1 / 13,
    HandState.NINE: 1 / 13,
    HandState.FIGURE: 4 / 13,
}

# State after a split for each pocket pairs states
POST_SPLIT_STATE = {
    HandState.POCKET_ACE: HandState.ACE,
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

# Moves
MOVE_STAND = "S"
MOVE_HIT = "H"
MOVE_DOUBLE = "D"
MOVE_SPLIT = "Sp"
MOVE_DOUBLE_ELSE_STAND = "D-S"
MOVE_DOUBLE_ELSE_HIT = "D-H"
MOVE_SURRENDER_ELSE_HIT = "U-H"
MOVE_SURRENDER_ELSE_STAND = "U-S"
MOVE_SURRENDER_ELSE_SPLIT = "U-Sp"

# Start hands probabilities factor (weights)
# 1 => probability of having a given set of 2 non ten-valued card (for example 2 & 2 or 5 & 7 or A & A or A & 7)
START_HAND_WEIGHTS = {
    # HandState.TWO is excluded, it is considered as a pocket A
    # HandState.THREE is excluded, it is considered as a pocket 3
    # HandState.FOUR is excluded, it is considered as a pocket 4
    HandState.FIVE: 2,  # 2 & 3,
    HandState.SIX: 2,  # 4 & 2, pocket 3 is excluded here
    HandState.SEVEN: 4,  # 5 & 2 or 4 & 3,
    HandState.EIGHT: 4,  # 6 & 2 or 5 & 3, pocket 4 is excluded here
    HandState.NINE: 6,  # 5 & 4 or 6 & 3 or 7 & 2,
    HandState.TEN: 6,  # 6 & 4 or 7 & 3 or 8 & 2, pocket 5 is excluded here
    HandState.ELEVEN: 8,  # 6 & 5 or 7 & 4 or 8 & 3 or 9 & 2,
    HandState.TWELVE: 14,  # F(10 or K or Q or J) & 2 or 9 & 3 or 8 & 4 or 7 & 5, pocket 6 is excluded here
    HandState.THIRTEEN: 14,  # F(10 or K or Q or J) & 3 or 9 & 4 or 8 & 5 or 7 & 6,
    HandState.FOURTEEN: 12,  # F(10 or K or Q or J) & 4 or 9 & 5 or 8 & 6, pocket 7 is excluded here
    HandState.FIFTEEN: 12,  # F(10 or K or Q or J) & 5 or 9 & 6 or 8 & 7,
    HandState.SIXTEEN: 10,  # F(10 or K or Q or J) & 6 or 9 & 7, pocket 8 is excluded here
    HandState.SEVENTEEN: 10,  # F(10 or K or Q or J) & 7 or 9 & 8,
    HandState.EIGHTEEN: 8,  # F(10 or K or Q or J) & 8, pocket 9 is excluded here
    HandState.NINETEEN: 8,  # F(10 or K or Q or J) & 9,
    # HandState.TWENTY is excluded, it is considered as a pocket figures,
    HandState.BLACKJACK: 8,  # F(10 or K or Q or J) & A,
    HandState.POCKET_ACE: 1,  # A & A,
    HandState.POCKET_TWO: 1,  # 2 & 2,
    HandState.POCKET_THREE: 1,  # 3 & 3,
    HandState.POCKET_FOUR: 1,  # 4 & 4,
    HandState.POCKET_FIVE: 1,  # 5 & 5,
    HandState.POCKET_SIX: 1,  # 6 & 6,
    HandState.POCKET_SEVEN: 1,  # 7 & 7,
    HandState.POCKET_EIGHT: 1,  # 8 & 8,
    HandState.POCKET_NINE: 1,  # 9 & 9,
    HandState.POCKET_FIGURE: 16,  # F(10 or K or Q or J) & F(10 or K or Q or J)
    # HandState.TWO_TWELVE is excluded, it is considered as a pocket A
    HandState.THREE_THIRTEEN: 2,  # A & 2,
    HandState.FOUR_FOURTEEN: 2,  # A & 3,
    HandState.FIVE_FIFTEEN: 2,  # A & 5,
    HandState.SIX_SIXTEEN: 2,  # A & 5,
    HandState.SEVEN_SEVENTEEN: 2,  # A & 6,
    HandState.EIGHT_EIGHTEEN: 2,  # A & 7,
    HandState.NINE_NINETEEN: 2,  # A & 8,
    HandState.TEN_TWENTY: 2,  # A & 9,
}
TOTAL_WEIGHTS_SUM = sum(START_HAND_WEIGHTS.values())  # 99
START_HAND_PROBABILITIES = {
    key: value / TOTAL_WEIGHTS_SUM for key, value in START_HAND_WEIGHTS.items()
}


# Signatures, used determine the hand knowing the 2 constituting cards
# use power of 2 to enable use of binary masks
CARD_SIGNATURES = {
    HandState.TWO: 0,
    HandState.THREE: 1,
    HandState.FOUR: 2,
    HandState.FIVE: 4,
    HandState.SIX: 8,
    HandState.SEVEN: 16,
    HandState.EIGHT: 32,
    HandState.NINE: 64,
    HandState.FIGURE: 128,
    HandState.ACE: 256,
}
