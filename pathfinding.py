from collections import deque


class PathFinding:
    def __init__(self, game):
        self.game = game
        # self.game.map.load_from_file(DEFAULT_MAP_PATH)
        # self.map = game.map.mini_map
        self.map = [row[:] for row in self.game.map.mini_map]
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()
        self.visited = None

    def get_path(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            return start

        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        return visited

    def get_next_node(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if col in (0, 4, 5, 6):
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_node(x, y)