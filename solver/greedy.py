from animation.animator import State, Animator


class GreedySolver:
    def __init__(self, state):
        pass

    def solve(self, state):
        # lets try an algorithm that works for most cases.
        # n-agent tsp
        routing = []
        t = 0
        nr_robots = len(state.robot_pos)
        agents = [(i, [state.robot_pos[i]]) for i in range(nr_robots)]
        free_agents = {0: list(range(nr_robots))}
        items = state.item_pos[:]
        while len(items) > 0:
            for agent_index in free_agents.get(t, [])[:]:
                agent = agents[agent_index]
                min_dist = 10**100
                best_item = 0
                if len(items) == 0:
                    break
                for item_index,item in enumerate(items):
                    d = self.dist(item, agent)
                    if d < min_dist:
                        min_dist = d
                        best_item = item_index
                agent[1].append(items[best_item])
                del items[best_item]  # slow delete
                free_agents[t].remove(agent[0]) # slow delete
                new_t = t + min_dist
                if new_t not in free_agents:
                    free_agents[new_t] = []
                free_agents[new_t].append(agent[0])
            t += 1 # store keys in heap
        max_t = max(free_agents.keys())
        routing = self.assignment_to_routing(agents, max_t)
        return routing

    def assignment_to_routing(self, agents, max_t):
        routing = [[] for i in range(max_t+1)]
        for agent in agents:
            assignment = agent[1]
            start = assignment[0]
            t = 0
            for item in assignment[1:]:
                x = item[0] - start[0]
                for i in range(abs(x)):
                    if x > 0:
                        routing[t].append((1,0))
                    else:
                        routing[t].append((-1,0))
                    t+=1

                y = item[1] - start[1]
                for i in range(abs(y)):
                    if y > 0:
                        routing[t].append((0, 1))
                    else:
                        routing[t].append((0, -1))
                    t+=1
                start = item
            for i in range(t,max_t):
                routing[i].append((0,0))
        return routing

    def dist(self, item, agent):
        agent_pos = agent[1][-1]
        return abs(item[0]-agent_pos[0]) + abs(item[1] - agent_pos[1])




if __name__ == '__main__':
    state = State(30,10)
    state.add_robot(2)
    state.add_items(12)
    solver = GreedySolver(state)
    routing = solver.solve(state)
    print(routing)
    animator = Animator()
    animator.run_routing(state, routing)

