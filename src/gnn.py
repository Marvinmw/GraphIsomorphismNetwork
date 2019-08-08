import numpy as np
import torch
import molecule

class GraphIsomorphismNetwork:
    def __init__(self, node_dim, update_loop_size):
        self.node_dim = node_dim
        self.update_loop_size = update_loop_size
        self.eps = np.random.normal() # learnable parameter    

    # function to update nodes
    def mlp(self, molecule):
        next_nodes = torch.zeros_like(molecule.nodes)
        for i in range(next_nodes.shape[0]):
            next_nodes[i] = (torch.t(molecule.graph[i]) * molecule.nodes).sum(dim=1)
        return (1.0 + eps)*molecule.nodes + next_nodes

    def readout(self, molecule):
        return molecule.nodes.sum(dim=0)

    def predict(self, molecule):
        
        # CONCAT(READOUT(molecule.nodes at k) k < update_loop_size)
        sum_of_node = torch.zeros(self.node_sim)        
        for i in range(update_loop_size):
            molecule.nodes = self.mlp(molecule) 
            sum_of_nodes += self.readout(molecule)

        return sum_of_nodes