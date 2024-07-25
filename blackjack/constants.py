from enum import Enum


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

# All hard stated for a player
PLAYER_HARD_STATES = [
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
]

# All soft states for a player
PLAYER_SOFT_STATES = [
    HandState.TWO_TWELVE,
    HandState.THREE_THIRTEEN,
    HandState.FOUR_FOURTEEN,
    HandState.FIVE_FIFTEEN,
    HandState.SIX_SIXTEEN,
    HandState.SEVEN_SEVENTEEN,
    HandState.EIGHT_EIGHTEEN,
    HandState.NINE_NINETEEN,
    HandState.TEN_TWENTY,
]

# All player pocket pairs state
PLAYER_PAIRS_STATES = [
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
