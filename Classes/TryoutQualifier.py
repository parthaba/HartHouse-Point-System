from Classes.Team import Team
from Classes.Qualifier import Qualifier


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
    _max_points = int

    def __init__(self, number_of_teams: int, limit: int, rounds: int, rooms: int) -> None:
        super().__init__(number_of_teams, limit)
        self._max_points = rounds * 3
        self.rooms = rooms
        self.field = self.determine_field()

    def pre_tryout(self) -> dict:
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

        Qualifier.compile_teams(self)

        team_requirements = {}
        for team in self.team_ranks[:self.limit]:
            team_requirements[team.team_name] = self.find_when_baller(team)

        return team_requirements

    def post_tryout(self):
        """Update self.team_points and self.team_ranks. Display the qualifying teams that get a spot."""
        # TODO: Implement this method
        ...

    def determine_field(self):
        """Determine the field for this qualifier."""
        sum_top_teams = 0

        for x in range(self.limit):
            sum_top_teams += self.team_points[self.team_ranks[x]]

        return sum_top_teams / len(self.teams)

    def is_team_baller(self, team: Team, determined_gap: float) -> bool:
        """Determine which team(s) qualify for the tournament regardless of how
        they do in the qualifier."""

        # In order for team to not qualify, self.limit other debate teams would have to rank above them in competitive
        # points after the tryout is over. If that is impossible because the other debate teams' points are too low,
        # team will qualify no matter what.

        # Getting the total competitive points of team
        baller_team_points = self.team_points[team]

        # Creating a new list of the top self.limit debate teams, excluding team.
        next_highest_teams = self.team_ranks[:]
        next_highest_teams.remove(team)
        next_highest_teams = next_highest_teams[:self.limit]

        # Measuring the combined gap between team and the other debate teams in next_highest_teams
        total_gap = 0
        for current_team in next_highest_teams:
            current_team_points = self.team_points[current_team]
            current_gap = baller_team_points - current_team_points
            total_gap += current_gap

        # If total_gap > determined_gap, then it is impossible for team to be knocked out of the qualifier.
        return total_gap > determined_gap

    def find_when_baller(self, team: Team) -> int:
        """Calculate how many points a team would need to ball out (qualify regardless of what else happens)."""

        # biggest_possible_gap is the maximum amount of additional competitive points the other teams can acquire
        # throughout the course of the tryout. This is calculated by taking the 'competitive value' of each tryout
        # point (field/maximum points) and multiplying it by the total number of points given out
        # at the tryout (rooms*rounds*6). Maximum points can be calculated as rounds*3.
        value_of_point = self.field / (self.rounds * 3)
        total_points = self.rooms * self.rounds * 6

        balling = False              # loop condition: when a team balls out, balling= True
        earned_points = 0           # accumulator for how many points a team would have to earn to ball out

        # Continue adding points to team until they ball out. Return the number of points they needed.
        while not balling:
            current_largest_gap = value_of_point * (total_points - earned_points)

            if self.is_team_baller(team, current_largest_gap):
                balling = True
            else:
                earned_points += 1

        return earned_points