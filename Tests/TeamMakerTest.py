from Classes.TeamMaker import TeamMaker
from Classes.Qualifier import Qualifier
import unittest


class TestTeamMaker(unittest.TestCase):
    team_list = [[463871, 119567], [829380, 459855]]
    new_qual_contingent = TeamMaker(3)
    new_qual_contingent.team_list = team_list

    new_qual = Qualifier

    def test_create_team_list(self):
        contingent_list = self.new_qual_contingent.create_team_list()
