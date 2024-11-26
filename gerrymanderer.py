import random
from electorate import Electorate

class Gerrymanderer():
    def __init__(self, electorate):
        self.electorate = electorate
        self.d = electorate.district_size()
        self.marked = [False for _ in self.electorate.graph.adj]
        self.number_visited = 0
        self.depth = 0
        self.districts = []

    def visited_setup(self):
        visited = [False] * (self.d ** 2)
        i = 0
        while i < self.d ** 2:
            if self.marked[i] == True:
                visited[i] = True
            i += 1
        return visited


    def gerrymander(self):
        while self.number_visited < (self.d ** 2):
            r = random.randint(0, self.d ** 2 - 1)
            while self.marked[r] is True:  
                r = random.randint(0, self.d ** 2 - 1)
            visited = self.visited_setup()
            # horrible way this is nested. first sees if it can narrowly win a district at r, then sees if it can 
            # lose a district badly, then maks a random district. has to reset visited each time using visited_setup
            district = self.dfs_win(r, 0, [], visited)
            if district:
                for i in district:
                    self.marked[i] = True
                self.districts.append(district)
            else:
                visited = self.visited_setup()
                district = self.dfs_lose(r, 0, [], visited)
                if district:
                    for i in district:
                        self.marked[i] = True
                    self.districts.append(district)
                else:
                    visited = self.visited_setup()
                    district = self.dfs_random(r, [], visited)
                    if district is None:
                        return self.districts
                    for i in district:
                        self.marked[i] = True
                    self.districts.append(district)
            self.number_visited += self.d
        return self.districts
            
    def dfs_win(self, v: int, true_count: int, district: list, visited: list):
        visited[v] = True
        for w in self.electorate.graph.adj[v]:
            if len(district) == self.d:
                return district
            if not visited[w]:
                # bad-ish algorithm, throws out a lot of cases that could work so will be None in most cases
                if true_count < self.d // 2 + 1:
                    if self.electorate.votes[w]== True:
                        true_count += 1
                        district.append(w)
                    else:
                        return
                else:
                    if self.electorate.votes[w] == True:
                        return
                    else:
                        district.append(w)
                self.dfs_win(w, true_count, district, visited) 
    
    def dfs_lose(self, v: int, false_count: int, district: list, visited: list):
        visited[v] = True
        for w in self.electorate.graph.adj[v]:
            if len(district) == self.d:
                return district
            if not visited[w]:
                # this one throws out even more cases than dfs_win. lol
                if self.electorate.votes[w] == True:
                    return
                else:
                    district.append(w)
                self.dfs_lose(w, false_count, district, visited)

    def dfs_random(self, v: int, district: list, visited: list):
        visited[v] = True
        for w in self.electorate.graph.adj[v]:
            if len(district) == self.d:
                return district
            if not visited[w]:
                district.append(w)
                self.dfs_random(w, district, visited)
        


# e = Electorate(9)
# print(e.graph.adj)
# g = Gerrymanderer(e)
# print(g.marked)

# e = Electorate(3)
# print(e.graph.adj)
# print(e.votes)
# g = Gerrymanderer(e)
# print(g.gerrymander())

