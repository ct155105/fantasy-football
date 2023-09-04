
# Player has float ppg and float likelihood_of_playing
class Player:
    def __init__(self, name: str, ppg: float, likelihood_of_playing: float):
        self.name = name
        self.ppg = ppg
        self.likelihood_of_playing = likelihood_of_playing

    def __repr__(self):
        return f"Player(ppg={self.ppg}, likelihood_of_playing={self.likelihood_of_playing})"
