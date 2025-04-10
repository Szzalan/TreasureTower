class PlayerState:
    def __init__(self,current_health,gold,max_health=150, potion_amount=0):
        self.max_health = max_health
        self.current_health = current_health
        self.gold = gold
        self.potion_amount = potion_amount