import random
from electorate import Electorate

class Gerrymanderer():
    def __init__(self, electorate):
        self.electorate = electorate
        self.d = electorate.district_size()
        self.marked = [False for _ in self.electorate.graph.adj]
        self.checked = [False for _ in self.electorate.graph.adj]
        self.number_visited = 0
        self.count = 1
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
        # While the number of districts is less than d, the desired number of districts:
        while len(self.districts) < self.d - 1:
            # generate a random index and see if there's already a district there, loop until you
            # get a valid index
            r = random.randint(0, self.d ** 2 - 1)
            while self.marked[r] is True:  
                r = random.randint(0, self.d ** 2 - 1)

            # Reset visited and see if you can make a narrowly winning district
            visited = self.visited_setup()
            district = self.dfs_win(r, 0, [r], visited)
            if district:
                pass
            else:
                # otherwise see if you can make a badly losing district
                visited = self.visited_setup()
                district = self.dfs_lose(r, 0, [r], visited)
                if district:
                    pass
                # otherwise generate a random district
                else:
                    visited = self.visited_setup()
                    district = self.dfs_random(r, [r], visited)
                    print(district)

            # This next if will be eliminated in the final code because district never should be None by this point.
            # For now just avoids throwing an error
            if district is None:
                continue
            
            # Update self.marked
            for i in district:
                self.marked[i] = True

            # Initialize self.checked, basically just self.marked but gets resetted every loop.
            # Tells what chunks of False have been checked (counted) to make sure that there's not a choke
            # point where some constituents won't be able to join a vaild district
            self.checked = self.visited_setup()
            i = 0
            while i < len(self.checked):
                self.count = 1
                # If it's already got a district there, increment and continue
                if self.checked[i] == True:
                    i += 1
                    continue
                # If it doesn't have a district there, count the number of constituents that can be
                # reached from this index
                else:
                    self.dfs_count(i)
                # Then if that count isn't divisible by self.d, fix self.marked and break.
                if self.count % self.d != 0:
                    for i in district:
                        self.marked[i] = False
                    break
                i += 1
            # If after all of that you end up with a valid district, add it to districts
            if i == len(self.checked):
                self.districts.append(district)
        district = []
        for i in range(len(self.marked)):
            if self.marked[i] == False:
                district.append(i)
        self.districts.append(district)
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
                        continue
                else:
                    if self.electorate.votes[w] == True:
                        continue
                    else:
                        district.append(w)
                self.dfs_win(w, true_count, district, visited) 
            return None
    
    def dfs_lose(self, v: int, false_count: int, district: list, visited: list):
        visited[v] = True
        for w in self.electorate.graph.adj[v]:
            if len(district) == self.d:
                return district
            if not visited[w]:
                # this one throws out even more cases than dfs_win. lol
                if self.electorate.votes[w] == True:
                    continue
                else:
                    district.append(w)
                self.dfs_lose(w, false_count, district, visited)
            return None

    def dfs_random(self, v: int, district: list, visited: list):
        visited[v] = True
        for w in self.electorate.graph.adj[v]:
            if len(district) == self.d:
                print(district)
                return district
            if not visited[w]:
                district.append(w)
                self.dfs_random(w, district, visited)
    
    def dfs_count(self, v: int):
        self.checked[v] = True
        for w in self.electorate.graph.adj[v]:
            if not self.checked[w]:
                self.count += 1
                self.dfs_count(w)
        


# e = Electorate(9)
# print(e.graph.adj)
# g = Gerrymanderer(e)
# print(g.marked)

# e = Electorate(3)
# print(e.graph.adj)
# print(e.votes)
# g = Gerrymanderer(e)
# print(g.gerrymander())

