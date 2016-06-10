class CSP(search.Problem):
    def __init__(self, var, domains, neighbors, constrains):
        vars = var or domains.key()
        update(self, vars = vars, domains = domains, neighbor = neighbors,
                initial={}, curr_domians = None, pruned=None, nassigns = 0)

    def assign(self, var, val, assignment):
        self.nassigns+ = 1
        assignment[var] = val
        if self.curr_domains:
            if self.fc:
                self.foward_check(var, val, assigment)
            if self.mac:
                AC3(self, [(Xk, var) for Xk in self.neighbors[var]])
    def unassign(self, var, assignment):
        if var in assignment:
            if self.cutt_domains[var] = self domains[var][:]
        del assignment[var]

    def nconflicts(self,var, val, assignment):
        def conflict(var2):
            val2 = assignemnt.get(var2, None)
            return val2 != None and self.constrains(var, val, var2, val2 )
        return count_if(conflict, self.neighbors[var])

    def forward_check(self, var, val, assignment):


def updateDict(key, val, dict):
    if key not in dict:
        dict[key]=[]
    dict[key]=val
    return dict

def updateDictWithKeyAndVal(keyValueArray, Dict):
    dict=Dict[:]
    key, vals = keyValueArray
    if key not in dict:
        dict[key]=[]
    valsArray = map(lambda x: splitVal(x), vals)
    useKeyForDictKey = map(lambda x: updateDictWithKeyAndVal(key, x, dict), valsArray)
    useValueForDictKey = map(lambda x: updateDictWithKeyAndVal(x, key, useKeyForDictKey), valsArray)
    return useValueForDictKey

def splitVal(val):
    return val.split()

def parse_neighbors(neighbors, vars=[]):
    vals = [key.split(': ') for key in neighbors.split('; ')]
    print vals
    newDict = reduce(lambda x,y: updateDictWithKeyAndVal(x, y),vals,{})
    return newDict
