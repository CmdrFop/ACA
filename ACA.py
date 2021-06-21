from typing import List
import itertools
import numpy as np


class CM:
    def __init__(self, matrix, lexicon, nodes, selected_node, referents):
        self.matrix = matrix
        self.lexicon1 = lexicon
        self.lexicon2 = lexicon
        self.nodes = nodes
        if selected_node:
            self.index = nodes.index(selected_node)
            nodes.remove(selected_node)
            combinations = [list(zip(nodes, x)) for x in
                            itertools.product([True, False], repeat=len(nodes))]
            for comb in range(len(combinations)):
                combinations[comb].insert(self.index, (selected_node, True))
            self.combinations = combinations
        else:
            self.index = -1
        self.referents = referents

    def runCM(self):
        coherence_values = []
        Node = self.index
        for comb in self.combinations:
            coherence_sum = 0.0
            for node_i in range(len(self.nodes)+1):
                for node_j in range(len(self.nodes)+1):
                    weight = 1.0
                    if node_i == Node or node_j == Node:
                        weight = weight * (len(self.nodes)+1)
                    if comb[node_i][1] == comb[node_j][1] and node_i != node_j and self.matrix[node_i][node_j] == 1:
                        coherence_sum += 1.0 * weight
                    elif comb[node_i][1] != comb[node_j][1] and node_i != node_j and self.matrix[node_i][node_j] == -1:
                        coherence_sum += 1.0 * weight

            coherence_values.append(coherence_sum)

        max_is = max(coherence_values)/ len(self.nodes)
        index = np.argmax(coherence_values)
        #print(self.combinations[index])
        references = [x[1] for x in self.combinations[index][:len(self.referents)]]
        values = [1.0 if x is True else 0.0 for x in references]
        end_result = np.dot(max_is, values)

        for row in range(len(self.lexicon1)):
            for i in range(len(self.lexicon1)):
                if end_result[i] > 0:
                    self.lexicon1[row][i] = self.lexicon1[row][i] * end_result[i]
        return self.lexicon1






