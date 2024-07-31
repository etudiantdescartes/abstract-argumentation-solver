# Abstract Argumentation Framework Solver

The objective is to find various structures in an abstract argumentation framework represented as a graph.

The graph is represented by an adjacency matrix. Arcs are represented by the value 1 in the matrix, and the rest is 0. So for a matrix M, if M[i,j] = 1, node i attacks node j.
Conflict-free Sets

First, we look for conflict-free sets among all combinations of nodes. We eliminate all combinations such that:
There exists at least one case where: i and j belong to this combination and M[i][j] = 1.

# Admissible Sets

Next, we find all sets that defend themselves against their attackers among the remaining combinations. For each set, we verify:
For each node j in the set to be verified, for each node i in the graph, if i attacks j (i.e., M[i][j] = 1):
We check for each node k in the set if M[k][i] = 1. It is sufficient for i to be attacked once by an element of the set to satisfy this condition.

# Complete Extensions

A function checks if a node entered as a parameter is defended by a node from a given set, as described previously.
In a second function, we call the first function for each node in the graph: if the node is defended against all its attackers by the set without belonging to it, then we reject this set.
We can then call the second function for each combination. This allows us to determine if the combination of nodes is a complete extension.

# Stable Extensions

We define a function to check if a list passed as a parameter (complete extension) attacks all nodes outside this list:
For each node in the graph, if it is not in the list, we check if it is attacked by at least one node from the list. If this is the case, the function returns True. If there is even a single node not attacked by the set, we exit the loop and reject this set.

# DC-ST / DC-CO

To determine if an argument is credulously accepted:
We iterate through the list of combinations, applying the previously defined functions to check if a set is admissible and a complete extension (for stable extensions, we also call the associated function).
We then check if the argument is in the extension. If it is, we return YES; otherwise, we continue to iterate through the sets.

# SE-ST

To find a stable extension, the function is similar to the one described above, without checking for the presence of an argument in the extension.
# SE-CO

For the SE-CO option, we calculate the grounded extension:
First, we get the list of all nodes that are not attacked (i.e., all nodes for which the sum of the elements in the corresponding column in the matrix is 0).
We iterate through this list and reject all attacked nodes.
We then add all nodes that are not attacked (and not rejected) to the list of accepted elements.
We repeat these operations until the length of the list of accepted elements no longer changes.

# DS-CO

First, we check if the grounded extension is empty: if so, we return ‘NO’. Otherwise, as with the algorithms used for DC-ST and DC-CO, we retrieve the complete extensions among the combinations of nodes. If we find a complete extension in which the argument is not present, we return ‘NO’. We return ‘YES’ at the end of the function.
# DS-ST

The principle is the same, verifying if the extensions are stable. Moreover, if we do not find a stable extension, and the argument is indeed part of the graph, we return ‘YES’.
