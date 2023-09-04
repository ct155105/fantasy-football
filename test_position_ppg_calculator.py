from position_ppg_calculator import PositionPpgCalculator
from models.player import Player


def test_calculate_position_ppg() -> None:
    # Arrange
    starters_at_position = 2
    players = [
        Player("Player 1",20,.5),
        Player("Player 2",10,.5),
        Player("Player 3",5,.5),
        Player("Player 4",1,.5)
    ]
    expected = 18

    # Act
    actual = PositionPpgCalculator(starters_at_position, players).calculate_position_ppg()

    # Assert
    assert actual == expected
    