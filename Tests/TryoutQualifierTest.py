from Classes.TryoutQualifier import TryoutQualifier
import unittest


class TestTryoutQualifier(unittest.TestCase):
    # Create TryoutQualifier object for Cambridge IV Quals
    team_list = [
        [463871, 357944],  # Arpi and Serena
        [919543, 756779],  # McEwen and Pranav
        [251130, 919974],  # Eamon and Kathryn
        [547963, 286520],  # Matt and Muzzi
        [243512, 873585],  # Adam and Tanvir
        [522130, 826186],  # Mia and Valerie
        [916092, 653024],  # Dihan and Farhan
        [588665, 313361]   # Elgin and Boomba
    ]
    cambridge_qual = TryoutQualifier(8, 4, 2, 2)
    cambridge_qual.set_team_list(team_list)

