
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/11iqoKeVibg/0.jpg)](http://www.youtube.com/watch?v=11iqoKeVibg)

# Outline:
- A visualisation tool that helps users understand how classical path-finding algorithms such as the Dijkstra algorithm, the Bidirectional Dijkstra algorithm and the A* search algorithm work by viewing them in action. These algorithms (and their optimizations) are widely used in popular mapping tools such as Google Maps and Yandex.
- Users can choose a start node and an end cell, add walls to block off paths and add bombs to make certain cells more expensive to use and then visualise how these algorithms explore the graph and locate the shortest path. Users can also run different algorithms on the same grid that they have populated with specific walls and bombs in order to compare the procedure of algorithms.
- The video above illustrates how the path-finding tool, built using Tkinter and PyGame, works and showcases its clean design and friendly UI.
- A detailed description about the build as well as the algorithms themselves can be found down below.

# Purpose:
- While resources on how to program these classical algorithms and understand how they came to be are widely available, I find that I am largely a visual learner and thus learn better when I can see the algorithm first-hand and understand its nuances by tinkering with it, therefore I wanted to come up with my own visualisation tool.
- I had learnt these algorithms as part of the [Data Structures and Algorithms Specialisation](https://www.coursera.org/specializations/data-structures-algorithms) by UCSD and HSE on Coursera but I found that the programming assignments for those courses were slightly incomplete as they didn't involve getting the input and sifting through it to create some meaningful data structure that I could employ for the graph and therefore I wanted to give users a sandbox environment where they could add their own walls and bombs to create scenarios more reflective of real life, and this situation would also force me to understand how to efficiently process the data and convert it to a meaningful data structure. Pygame offered itself as the perfect tool to both get user data as well as to display the path-finding process and Tkinter made the menu-driven set-up process very easy.
- I chose the Dijkstra and A* Algorithm as there are the cornerstones of classical path-finding (alongside other algorithms such as the Bellman-Ford) and the Bi-Dijkstra variant is very popular in dealing with social networks and yielded a very interesting visualisation scenario - more on that below.
- The build was very engaging and forced me to reckon with abstract concepts such as complexity of both time and space in order to make sure my algorithms were reflective, in some part, of the real world applications. Moreover, designing a clean, minimal UI that captivated users forced me to understand how colours complement each other and their effect on the human psyche.

# Description:
- In case you are only interested in the description of the algorithms, you can access them here:
    - [Dijkstra](https://github.com/akashvshroff/Path_Finding_Visualisation#dijkstra)
    - [Bi-Dijkstra](https://github.com/akashvshroff/Path_Finding_Visualisation#bi-dijkstra)
    - [A* Search](https://github.com/akashvshroff/Path_Finding_Visualisation#a-search)
- Before I delve into the build - with the corresponding pygame event loops and tkinter setup - I want to address the file structure.
- The UI comprising of the Tkinter window(s) and the pygame screen is housed in the path_finding.py file.
- Each of the algorithms are classes in their individual files and each of these have methods and attributes which share names. in order to ensure that the algorithm choice doesn't alter how the path_finding file accesses methods and attributes. Moreover, each of these classes have different methods for solving with visualising and without - this is something I could have avoided with a conditional and a return statement but I've consciously separated them so that it  is easier to understand how running the algorithm corresponds to the pygame event loop.
- On running, the user is first greeted by a tkinter window that explains the process and gets the input for the algorithm and whether they want to see the visualisation screen - by way of a dropdown menu and checkbox.
- An instance of the pygame class is created using the data that the user enters and then the user input for the path-finding components that is the source, target, walls and bombs is gotten - at each step, instructions are provided to make it easier for any user.
- The pygame class operates using 4 event loops:
    - The user input loop which is housed in the get_user_input method where mouse presses etc are all handled as the user picks the components.
    - The solve with visualisation loop which gets the visited cells from the object of the algorithm chosen and displays them.
    - The solve without visualisation loop which has no visualisation and therefore just calls upon the algorithm and once it is over, it calls the solved loop.
    - The solved loop which is called by the solve (with or without visualisation) displays the path found if any, or shows a message saying that no path exists. If a path is present, it also indicates the cost and number of cells used. Here, users are given the option to re-run on the same grid using a different algorithm or simply reset the entire grid and run again.
- All the pygame loops use the same function draw_grid to display the messages, the grid and all its components (bombs, walls, start cell, end cell, visited cells during visualisation and the path if any etc) as well as the buttons to be displayed.
- Another tkinter window is displayed when the user wants to re-run or reset and here the user can select an algorithm again and whether they want visualisation.
- Once the user-data is gotten, the driver function which processes the data, creating both a cost matrix as well as the adjacency list for the connections, as well as creating the object of the necessary algorithm and using the appropriate event loop, is called.

## Algorithms:

- Below, I explain each of the algorithms used as well as some of the basic data structures used by each of the classes for the algorithms.

---
### Dijkstra:

- The classical Dijkstra's algorithm can be used to find the shortest path from the source vertex to any other vertex in a weighted graph and in that sense it is commonly referred to as a 'one source, many targets' algorithm.
- The algorithm only works on graphs that have edges with non-negative weights associated with them.
- The algorithm works effectively by building a set of nodes that have the minimum distance from the start vertex and maintains the distance from each vertex to the start vertex in an array (or dictionary/hash-map) dist where dist[v] refers to an upper-bound on the maximum distance between the start vertex s and vertex v. The array dist is generally initialised with the value positive infinity for each node except the start node.
- An important point to note is that in this algorithm, edges are *relaxed.* Suppose there exists a vertex v and a vertex u and there is an edge from u to v. To relax an edge is to choose whether the present path from start vertex s to v can be made better by including the vertex u and thus the edge u,v.
- This is done by checking if dist[v] is larger than dist[u] + the weight of the edge from u to v. If so, then dist[v] is reduced and prev, an array (or hash-map) which indicates how the vertex was reached and is used in reconstructing the path, is updated.

    ```python
    def relax(u,v):
       if dist[v] > dist[u] + weight_of_edge(u,v):
          dist[v] = dist[u] + weight_of_edge(u,v)
          prev[v] = u
    ```

- Now, in order to build a set of nodes that already have the minimum distance from the start vertex, you need to choose nodes that have the minimum dist value. And this can be done by maintaining a priority queue of the nodes.
- Thus the program becomes becomes:
    - While the queue is not empty:
        - Pop the smallest element.
        - Iterate over all its neighbours:
            - Relax the edge, if a vertex can get relaxed, change the priority of the vertex in queue to its new dist value.
    - Once all have been processed, reconstruct the optimal path.
- To reconstruct the shortest path, you can simply loop from the target vertex until you reach the source vertex:

    ```python
    vertex = target
    path = []
    while vertex != start:
      path.append(vertex)
      vertex = prev[vertex]
    path.reverse() # to get the order correct
    ```

- A priority queue maintained by a min heap ensures a complexity of O(n log n) versus one maintained using an array which would result in a complexity of O(n^2) and in this build, I used the priority queue implemented by the heapq library.
- Since changing the priority is time consuming, I maintain a hash-map proc which is true if a node has already been processed (if it has been popped from the queue and its neighbours have been relaxed) and therefore instead of changing priority, I can just add a new element to the queue with the new dist value.
- Moreover, to decrease runtime, instead of waiting until all nodes have been processed, I break the while loop if the end vertex has been processed.
- An excellent resource to know more about the Dijkstra algorithm is [here.](https://brilliant.org/wiki/dijkstras-short-path-finder/)

---
### Bi-Dijkstra:
- The Bidirectional Dijkstra algorithm is a modification of the regular Dijkstra algorithm and to understand it, it is easier to understand the working of the Dijkstra's algorithm.
- To understand how the Dijkstra's algorithm effectively works, we need to visualise the locations of the nodes that are processed (quite an apt time to tell you to use the tool I have made) and the best way to describe how the processed nodes grow over time is by imagining them as a circle of growing radius with the source vertex as the center and the circle continues to expand outwards until the target vertex is met or all vertices have been processed.
- In the bi-directional approach, you run Dijkstra's algorithm from both the source vertex as well as the target vertex and reconstruct a path when the two circles meet, i.e when one tries to process a node that the other has already processed.
- The middle node where the forward and backward Dijkstra meet provides an upper bound for the shortest distance but it isn't confirmed to be the shortest distance, that can be found by looping over all the processed nodes and calculating the shortest distance and identifying the best middle node.
- By using the forward and backward search, the number of nodes visited are almost half and while this does not lead to any complexity changes since it is a constant factor nor does it reflect too well on road networks, while traversing social networks, this change leads to exponential benefits owing to the ['Six Handshakes Theorem'](https://www.coursera.org/lecture/algorithms-on-graphs/six-handshakes-wcPrk).
- The data structures used are very similar to the Dijkstra algorithm and the two approaches, forward and backward, run turn by turn in the while loop.
- An excellent resource to understand the underlying mathematical theorems is [here.](https://www.coursera.org/lecture/algorithms-on-graphs/bidirectional-dijkstra-7ml18)
- Another excellent resource is this [article.](https://www.homepages.ucl.ac.uk/~ucahmto/math/2020/05/30/bidirectional-dijkstra.html)

---
### A* Search:
- The A* search algorithm is an enhancement of the Dijkstra algorithm that can lead to run-times of about 1/1000 times in real life usage and it does so by conducting a *directed search*.
- In the simplest of terms the algorithm works by knowing where the target vertex is and therefore the order in which it picks nodes and processes them varies based on this information. You then apply a potential function (or heuristic) which maps each node to some non-negative integer value. This value is then added in the queue for each node and therefore influences the order in which nodes are processed.
- In this example, since we can only move left, right, up and down, the heuristic employed is the Manhattan distance. This distance is the sum of the absolute value of the difference in x and y co-ordinates between 2 vertices.

    ```python
    def manhattan_distance(x1,x2,y1,y2):
        return abs(x1-x2) + abs(y1-y2)
    ```

- In this scenario, our potential function or heuristic is calculated for every node with respect to the target node and therefore nodes selected are based on their distance from the target node.
- This heuristic provides a lower bound for what the shortest between the node and the target node can be since it doesn't take into account any walls or bombs. And by using this heuristic to influence the selection of nodes means that the processed nodes are directed towards the target node.
- Another common heuristic employed in a scenario where movement in not restricted is the Euclidean distance which returns the shortest distance between 2 points on a map.

    ```python
    import math
    def euclid_distance(x1,x2,y1,y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    ```

- To learn more about the A* algorithm and other heuristics you can apply, check out this [article.](https://brilliant.org/wiki/a-star-search/)
