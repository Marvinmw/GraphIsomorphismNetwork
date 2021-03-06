import math
import torch
from ast import literal_eval
from molecule import *

def load_data():
    ### load data 
    #
    # Returns:
    #   list of Molecule: 
    #   list of torch.Tensor: 
    ###
    
    data_num = 1112

    graph_label_file = open('../dataset/PROTEINS/PROTEINS_graph_labels.txt')
    node_label_file = open('../dataset/PROTEINS/PROTEINS_node_labels.txt')
    node_attribute_file = open('../dataset/PROTEINS/PROTEINS_node_attributes.txt')
    graph_idx_file = open('../dataset/PROTEINS/PROTEINS_graph_indicator.txt')
    adjacency_file = open('../dataset/PROTEINS/PROTEINS_A.txt')

    # check graph size
    tmp0, tmp1 = 1, 1
    graph_list = [] # list of adjacency matrix
    graph_size_list = [] # list of total number of nodes that each graph has
    
    for graph_idx in range(data_num):
        graph_size = 1 # total number of nodes that graph has

        while True:
            tmp1 = int(graph_idx_file.readline())
            if (tmp0 == tmp1):
                graph_size += 1
                tmp0 = tmp1
            else:
                tmp0 = tmp1
                break

        # append adjacency matrix
        graph_list.append(torch.zeros(graph_size, graph_size))
        graph_size_list.append(graph_size)
        
    # chack adjacency matrix
    tmp_sum = 0
    tmp_sum1 = 0
    for graph_idx in range(data_num):
        tmp_sum += graph_size_list[graph_idx]
        
        while True:
            edge = literal_eval(adjacency_file.readline())
            if ((edge[0] <= tmp_sum) & (edge[1] <= tmp_sum)):
                graph_list[graph_idx][edge[0] - tmp_sum1][edge[1] - tmp_sum1] = 1.0
                graph_list[graph_idx][edge[1] - tmp_sum1][edge[0] - tmp_sum1] = 1.0
            else:
                break
        tmp_sum1 = tmp_sum

    print(graph_list[0])
        
    # check node feature
    node_dim = 4 # dimension of node
    node_list = []
    for graph_idx in range(data_num):
        nodes = torch.zeros(graph_size_list[graph_idx], node_dim)
        
        for node_idx in range(graph_size_list[graph_idx]):
            node_label = int(node_label_file.readline())
            node_attribute = float(node_attribute_file.readline())
            node_val =  1.0 #0.000000000000001
            if (node_label == 0):
                nodes[node_idx] = torch.tensor([node_val, 0.0, 0.0, node_attribute])
            elif (node_label == 1):
                nodes[node_idx] = torch.tensor([0.0, node_val, 0.0, node_attribute])
            else:
                nodes[node_idx] = torch.tensor([0.0, 0.0, node_val, node_attribute])
        node_list.append(nodes)


    # set molecule class
    molecule_list = []
    label_list = []
    for graph_idx in range(data_num):
        molecule_list.append(Molecule(graph_list[graph_idx], node_list[graph_idx]))
        label_list.append(torch.tensor([float(graph_label_file.readline()) - 1.0]).to('cuda'))

    graph_label_file.close()
    node_label_file.close()
    node_attribute_file.close()
    graph_idx_file.close()
    adjacency_file.close()

    return molecule_list, label_list

