class Bowler:
    def __init__(self, name, average):
        self.name = name
        self.average = float(average)


class Node:
    def __init__(self, cost, h_score, total_cost, runs, total_runs, over, parent_id):
        self.cost = cost
        self.total_cost = total_cost + cost
        self.h_score = h_score
        self.runs = runs
        self.total_runs = total_runs + runs
        self.over = over
        self.a_star_score = self.total_cost + self.h_score
        self.id = str(runs)+"-"+parent_id
        self.parent_id = parent_id

class AStar:
    def __init__(self, target, bowlers, bowling_order):
        self.target = target
        self.bowlers = bowlers
        self.bowling_order = bowling_order
        self.overs = len(bowling_order)

    def _calculate_cost(self, runs, average):
        return ((runs ** 2) / average)

    def _heuristic_score(self, runs_to_score, overs_remaining):
        if overs_remaining == 0:
            return 0
        total_average = 0
        for i in range(self.overs - overs_remaining, self.overs):
            total_average += self.bowlers[self.bowling_order[i]].average

        average_average = total_average / overs_remaining

        if runs_to_score < 0:
            runs_to_score = 0

        return (runs_to_score ** 2) / total_average

    def _create_level(self, selected_node):
        nodes = []
        over = selected_node.over + 1
        total_runs = selected_node.total_runs
        total_cost = selected_node.total_cost
        parent_id = selected_node.id

        for i in range(0, 37):
            cost = self._calculate_cost(
                i, self.bowlers[self.bowling_order[over-1]].average)

            h_score = self._heuristic_score(
                self.target - (total_runs + i), self.overs - over)

            nodes.append(Node(cost, h_score, total_cost, i, total_runs, over, parent_id))

        return nodes

    def find_combination(self):
        open_list = []
        closed_list = []
        root_node = Node(0, self._heuristic_score(self.target, self.overs), 0, 0, 0, 0, "root")

        open_list.append(root_node)

        while (len(open_list) != 0 and open_list[0].total_runs < self.target):
            selected_node = open_list[0]
            print(selected_node.id)
            if (selected_node.over == self.overs):
                open_list.pop(0)
                continue
            over_outcomes = self._create_level(selected_node)
            open_list.pop(0)
            closed_list.append(selected_node)
            open_list = open_list + over_outcomes
            open_list.sort(key=lambda e: e.a_star_score)

        goal = open_list[0]
        child = goal
        path = [goal]

        while (child.parent_id != "root"):
            for node in closed_list:
                if node.id == child.parent_id:
                    path.append(node)
                    child = node
                    break

        path.reverse()
        path.pop(0)
        return path

bowlers = [
    Bowler("Rashid Khan", 17),
    Bowler("Herath", 20),
    Bowler("Starc", 25),
    Bowler("Malinga", 15)
]

sample = AStar(60, bowlers, [0, 1, 2, 3])
path = sample.find_combination()
for node in path:
    print(node.id, node.total_cost, node.h_score, node.parent_id)
