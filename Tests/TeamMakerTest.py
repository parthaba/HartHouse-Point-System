from Classes.TeamMaker import TeamMaker
import unittest

class TestTeamMaker(unittest.TestCase):

    team_list = [[463871, 463871], [463871, 463871], [463871, 463871]]
    new_qual_contingent = TeamMaker(3)
    new_qual_contingent.team_list = team_list

    def test_create_team_list(self):
        contingent_list = self.new_qual_contingent.create_team_list()


