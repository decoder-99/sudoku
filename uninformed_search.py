from queue import Queue
from collections import deque


class Node:
    def __init__(self, parent, action, state):
        self.parent = parent
        self.action = action
        self.state = state


class Frontier:
    def add(self, node):
        pass

    def clear(self):
        pass

    def is_empty(self):
        pass

    def pop(self):
        pass

    def get_max_nodes_num(self):
        pass


class DepthFirstFrontier(Frontier):
    def __init__(self):
        self.stack = deque()
        self.max_count = 0

    def add(self, node):
        self.stack.append(node)
        self._check_stored_node_num()

    def clear(self):
        self.stack.clear()
        self.max_count = 0

    def is_empty(self):
        if self.stack:
            return False
        return True

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def get_max_nodes_num(self):
        return self.max_count

    def _check_stored_node_num(self):
        if self.max_count < len(self.stack):
            self.max_count = len(self.stack)


class BreadthFirstFrontier(Frontier):
    def __init__(self):
        self.queue = Queue()
        self.max_count = 0

    def add(self, node):
        self.queue.put(node)
        self._check_stored_node_num()

    def clear(self):
        self.queue = Queue()
        self.max_count = 0

    def is_empty(self):
        if self.queue.empty():
            return True
        return False

    def pop(self):
        if not self.is_empty():
            return self.queue.get()
        else:
            return None

    def get_max_nodes_num(self):
        return self.max_count

    def _check_stored_node_num(self):
        if self.max_count < self.queue.qsize():
            self.max_count = self.queue.qsize()


class Search:
    def find_solution(self, init_state, goal_test):
        pass

    @staticmethod
    def get_generated_nodes_num():
        pass


class TreeSearch(Search):
    def __init__(self, frontier):
        self.frontier = frontier
        TreeSearch.generated_num = 0

    def find_solution(self, init_state, goal_test):
        TreeSearch.generated_num = 0
        init_node = Node(None, None, init_state)
        self.frontier.add(node=init_node)
        TreeSearch.generated_num += 1
        while not self.frontier.is_empty():
            current_node = self.frontier.pop()
            if goal_test.is_goal(state=current_node.state):
                return current_node
            for action in current_node.state.get_applicable_actions():
                child_state = current_node.state.get_action_result(action)
                child_node = Node(current_node, action, child_state)
                self.frontier.add(child_node)
                TreeSearch.generated_num += 1
        return None

    @staticmethod
    def get_generated_nodes_num():
        return TreeSearch.generated_num


class GraphSearch(Search):
    def __init__(self, frontier):
        self.frontier = frontier
        GraphSearch.generated_num = 0

    def find_solution(self, init_state, goal_test):
        explored = set()
        GraphSearch.generated_num = 0
        init_node = Node(None, None, init_state)
        self.frontier.add(init_node)
        GraphSearch.generated_num += 1
        while not self.frontier.is_empty():
            current_node = self.frontier.pop()
            if current_node.state not in explored:
                if goal_test.is_goal(current_node.state):
                    return current_node
                explored.add(current_node.state)
                for action in current_node.state.get_applicable_actions():
                    child_state = current_node.state.get_action_result(action)
                    child_node = Node(current_node, action, child_state)
                    if child_state not in explored:
                        self.frontier.add(child_node)
                        GraphSearch.generated_num += 1
        return None

    @staticmethod
    def get_generated_nodes_num():
        return GraphSearch.generated_num
