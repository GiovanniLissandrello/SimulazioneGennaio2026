from model.model import Model

myModel = Model()
myModel.buildGraph(2007,2008)
nNodes, nEdges = myModel.getGraphDetails()
print(f"Num nodes: {nNodes}, num edges: {nEdges}")
myModel.filldob()
best, min = myModel.getPath(4)
for b in best:
    print(b)