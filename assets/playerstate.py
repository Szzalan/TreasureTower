class PlayerState:
    """
    Player State class

    Represents a player's current state.

    Attributes:
        max_health (int): Maximum health of the player.
        current_health (int): Current health of the player.
        gold (int): Amount of gold the player has.
        potion_amount (int): Amount of potions the player has.
        lucky_die_amount (int): Amount of lucky dice the player has.
    """
    def __init__(self,current_health,gold,max_health=150, potion_amount = 0, lucky_die_amount = 1):
        """
        Initializes the PlayerState object.

        Args:
            current_health (int): Current health of the player.
            max_health (int): Maximum health of the player.
            gold (int): Amount of gold the player has.
            potion_amount (int): Amount of potions the player has.
            lucky_die_amount (int): Amount of lucky dice the player has.
        """
        self.max_health = max_health
        self.current_health = current_health
        self.gold = gold
        self.potion_amount = potion_amount
        self.lucky_die_amount = lucky_die_amount