# %%
from simpleai.search import SearchProblem, astar, breadth_first, depth_first, uniform_cost
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer


class WaterJug(SearchProblem):
    def __init__(self, initial_state=(0, 0, 0), goal_state=(4, 4, 0), capacity=(8, 5, 3), is_cost_static=True):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.capacity = capacity
        self.is_cost_static = is_cost_static

    def actions(self, state):
        actions = []
        # fill
        if state[0] < self.capacity[0]:
            actions.append('fill 1')
        if state[1] < self.capacity[1]:
            actions.append('fill 2')
        if state[2] < self.capacity[2]:
            actions.append('fill 3')
        # empty
        if state[0] > 0:
            actions.append('empty 1')
        if state[1] > 0:
            actions.append('empty 2')
        if state[2] > 0:
            actions.append('empty 3')
        # pour
        if state[0] > 0 and state[1] < self.capacity[1]:
            actions.append('pour 1 2')
        if state[0] > 0 and state[2] < self.capacity[2]:
            actions.append('pour 1 3')
        if state[1] > 0 and state[0] < self.capacity[0]:
            actions.append('pour 2 1')
        if state[1] > 0 and state[2] < self.capacity[2]:
            actions.append('pour 2 3')
        if state[2] > 0 and state[0] < self.capacity[0]:
            actions.append('pour 3 1')
        if state[2] > 0 and state[1] < self.capacity[1]:
            actions.append('pour 3 2')
        return actions

    def result(self, state, action):
        state = list(state)
        action_key = action.split(' ')
        if action_key[0] == 'fill':
            state[int(action_key[1])-1] = self.capacity[int(action_key[1])-1]
        elif action_key[0] == 'empty':
            state[int(action_key[1])-1] = 0
        elif action_key[0] == 'pour':
            amount = min(state[int(
                action_key[1])-1], self.capacity[int(action_key[2])-1]-state[int(action_key[2])-1])
            state[int(action_key[1])-1] -= amount
            state[int(action_key[2])-1] += amount
        return tuple(state)

    def is_goal(self, state):
        return state == self.goal_state

    def cost(self, state, action, state2):
        if self.is_cost_static:
            return 1
        else:
            action_keys = action.split(' ')
            if action_keys[0] == 'fill':
                return self.capacity[int(action_keys[1])-1] - state[int(action_keys[1])-1]
            elif action_keys[0] == 'empty':
                return state[int(action_keys[1])-1]
            elif action_keys[0] == 'pour':
                return min(state[int(action_keys[1])-1], self.capacity[int(action_keys[2])-1]-state[int(action_keys[2])-1])
    def printer(statewithaction):
        state = statewithaction[1]
        action = statewithaction[0]
        action = str(action).split(' ')
        print(action,state)
        if action[0] == 'pour':
            print('Pour {} liters from jug {} to jug {}'.format(action[0], action[1], action[2]))
        elif action[0] == 'fill':
            print('Fill jug {}'.format(action[1]))
        elif action[0] == 'empty':
            print('Empty jug {}'.format(action[1]))
       


# %%
if __name__ == '__main__':
    my_viewer = BaseViewer()

    initial_state = (0, 0, 0)
    goal_state = (4, 4, 0)
    capacity = (8, 5, 3)

    problem = WaterJug(initial_state, goal_state,
                       capacity, is_cost_static=True)

    result = breadth_first(problem, graph_search=True, viewer=my_viewer)

    print(("Capacity:",capacity))
    for p in result.path():
        WaterJug.printer(p)
    print(my_viewer.stats)


# %%



