from models.player import Player


class PositionPpgCalculator:

    def __init__(self, starters_at_position: int, players: list[Player]):
        self.starters_at_position = starters_at_position
        self.players = players
        self.position_ppg = {}

    # The
    def calculate_position_ppg(self) -> dict[str, float]:
        total_ppg = 0
        starter_slots_filled = 0

        # sort players by ppg
        self.players.sort(key=lambda player: player.ppg, reverse=True)

        for player in self.players:
            if starter_slots_filled < self.starters_at_position:
                if starter_slots_filled + player.likelihood_of_playing < self.starters_at_position:
                    total_ppg += (player.ppg * player.likelihood_of_playing)
                    starter_slots_filled += player.likelihood_of_playing
                else:
                    remaining_playing_time = self.starters_at_position - starter_slots_filled
                    total_ppg += (player.ppg * remaining_playing_time)

        return total_ppg
