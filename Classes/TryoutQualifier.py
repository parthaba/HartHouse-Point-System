from typing import Dict

from Classes.Team import Team
from Classes.Qualifier import Qualifier
import math


class TryoutQualifier(Qualifier):
    """A subclass of the Qualifier parent class for qualifiers that require a tryout (rounds).

    Instance Attributes:
        - rounds: number of rounds held at the tryout
        - rooms: number of rooms

    Representation Invariants
        - rounds > 0
        - rooms > 0
        - field >= 0
    """
    rounds: int
    rooms: int
    field: float

    # Private Instance Attributes:
    #   - _max_points: maximum number of debate points a team can get at the tryout
    _max_points: int
    _value_of_each_point: float

    def __init__(self, number_of_teams: int, limit: int, rounds: int, rooms: int) -> None:
        super().__init__(number_of_teams, limit)
        self._total_qualifier_points = rounds * 6 * rooms
        self._max_points = rounds * 3
        self.rounds = rounds
        self.rooms = rooms

    def pre_tryout(self) -> None:
        """Display the pre-tryout rankings and qualification requirements for each team. Return
        it as a dictionary with each team as a key and their requirements as the respective
        key value.

        steps:
        - compile teams
        - show what each team needs to do to qualify
            - find what teams automatically qual
            - find what teams can qual if they get x points
            - other teams? probably not in limit
        """
        # TODO: Determine what this method needs and finish it.
        self.compile_teams()
        self.determine_field()

        team_requirements_baller = {}
        for team in self.team_ranks[:self.limit]:
            team_requirements_baller[team.team_name] = self.find_when_baller(team)

        team_requirements_not_baller = {}
        for team in self.team_ranks[self.limit:]:
            team_requirements_not_baller[team.team_name] = self.find_how_to_be_baller(team)

        print(team_requirements_baller)
        print(team_requirements_not_baller)

    def post_tryout(self, round_results: Dict[Team, int]):
        """Update self.team_points and self.team_ranks. Display the qualifying teams that get a spot."""

        # How many competitive points each qualifier point is worth
        points_per_point = self.field / self._max_points

        for team in round_results:
            team.working_point_total += round_results[team] * points_per_point

        super().display_qualifying_teams()

    def determine_field(self) -> float:
        """Determine the field for this qualifier."""
        sum_top_teams = 0

        for x in range(self.limit):
            sum_top_teams += self.team_ranks[x].working_point_total

        field = sum_top_teams / self.limit
        self.field = field
        return field

    def is_team_baller(self, team: Team, earned_points: int) -> bool:
        """Determine which team(s) qualify for the tournament regardless of how
        they do in the qualifier."""

        # # In order for team to not qualify, self.limit other debate teams would have to rank above them in competitive
        # # points after the tryout is over. If that is impossible because the other debate teams' points are too low,
        # # team will qualify no matter what.
        #
        # # Getting the total competitive points of team
        # baller_team_points = self.team_points[team]
        #
        # # Creating a new list that contains the next self.limit teams below team
        # team_index = self.team_ranks.index(team)
        # next_highest_teams = self.team_ranks[team_index:]
        # next_highest_teams.remove(team)
        # next_highest_teams = next_highest_teams[:(self.limit - team_index)]
        #
        # for team in next_highest_teams:
        #     print(team.team_name)
        #
        # # Measuring the combined gap between team and the other debate teams in next_highest_teams
        # total_gap = 0
        # for current_team in next_highest_teams:
        #     current_team_points = self.team_points[current_team]
        #     current_gap = baller_team_points - current_team_points
        #     total_gap += current_gap
        # print("Total Gap: " + str(total_gap))
        # print("Maximum Gap: " + str(maximum_gap))
        #
        # # If total_gap > maximum_gap, then it is impossible for team to be knocked out of the qualifier.
        # return total_gap > maximum_gap

        value_of_point = self.field / self._max_points
        team_to_beat = self.team_ranks[self.limit]
        if team.working_point_total + (earned_points * value_of_point) > \
                (team_to_beat.working_point_total + self.field):
            return True
        else:
            return False

    def find_when_baller(self, team: Team) -> int:
        """Calculate how many points a team would need to ball out (qualify regardless of what else happens)."""

        # biggest_possible_gap is the maximum amount of additional competitive points the other teams can acquire
        # throughout the course of the tryout. This is calculated by taking the 'competitive value' of each tryout
        # point (field/maximum points) and multiplying it by the total number of points given out
        # at the tryout (rooms*rounds*6). Maximum points can be calculated as rounds*3.

        balling = False  # loop condition: when a team balls out, balling= True
        earned_points = 0  # accumulator for how many points a team would have to earn to ball out

        # Continue adding points to team until they ball out. Return the number of points they needed.
        while (not balling) and (earned_points <= self._max_points):

            if self.is_team_baller(team, earned_points):
                balling = True
            else:
                earned_points += 1

        return earned_points

    def find_how_to_be_baller(self, team: Team) -> int:
        """For teams that wouldn't automatically qualify (i.e if their are 4 spots, all
        teams outside the top 4), returns the easiest path to qualifying
        (how many points they would need to beat the currently 4th ranked team)."""
        team_to_beat = self.team_ranks[self.limit - 1]
        point_deficit = team_to_beat.working_point_total - team.working_point_total

        value_of_point = self.field / self._max_points
        return math.ceil(point_deficit / value_of_point)

    def find_maximum_gap(self, team: Team) -> float:
        """Given a team, this method will find what the worst possible outcome of the qualifier
        is for that team. Then, it will return the total competitive point gap between the given
        team and other teams, not including pre-existing competitive points.

        For example, assume there is a qualifier with 8 teams competing, 4 spots available, 2 rooms and 2 rounds.
        Now imagine this method is called on the top ranked team. The method will assume the worst case: the next
        4 teams will be bracketed and place in such a way that it maximizes the number of points between the 4 of them.

        Note: I want to update this function later so that it also takes into account how those points are distributed,
        but for now I will keep it simpler."""

        # The number of teams that rank above the given team in points
        team_index = self.team_ranks.index(team)
        teams_above = team_index

        # Assume each of the teams that are in contention for a spot get max qual points
        number_of_teams_to_worry_about = self.limit - teams_above
        return self.field * number_of_teams_to_worry_about


team_list = [
    [239579, 158181],   # Anna and Amalie
    [463871, 357944],   # Arpi and Serena
    [412273, 242608],   # Emily and Cam
    [653024, 916092],   # Farhan and Dihan
    [431141, 919543],   # George and McEwen
    [738488, 816470],   # Hargun and Isabelle
    [949512, 620917],   # Jenkin and Nishka (need to add)
    [686446, 522130],   # Jessica and Valerie
    [919974, 251130],   # Kathryn and Eamon
    [927888, 605734],   # Simon and Akil
    [873585, 243512],   # Adam and Tanvir
    [563284, 715395],   # Zen and Yeni
]

wudc_qual = TryoutQualifier(12, 3, 3, 3)
wudc_qual.set_team_list(team_list)
wudc_qual.compile_teams()
print(wudc_qual)
print(wudc_qual.pre_tryout())
