import random
from electorate import Electorate

class Gerrymanderer():
    def __init__(self, electorate):
        self.electorate = electorate
        self.d = electorate.district_size()
        self.marked = [False for _ in self.electorate.graph.adj]
        self.number_visited = 0
        self.depth = 0


    def gerrymander(self):
        while self.number_visited < (self.d ** 2):
            r = random.randint(0, self.d ** 2 - 1)
            while self.marked[r] is True:  
                r = random.randint(0, self.d ** 2 - 1)
            return self.dfs_win(r, 0, 0, [])
            
    def dfs_win(self, v, true_count, false_count, district: list):
        self.marked[v] = True
        for w in self.electorate.graph.adj[v]:
            if len(district) == self.d:
                return district
            if not self.marked[w]:
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
                        false_count += 1
                        district.append(w)
                self.dfs_win(w, true_count, false_count, district) 
        


# e = Electorate(9)
# print(e.graph.adj)
# g = Gerrymanderer(e)
# print(g.marked)

e = Electorate(3)
print(e.graph.adj)
print(e.votes)
g = Gerrymanderer(e)
print(g.gerrymander())

