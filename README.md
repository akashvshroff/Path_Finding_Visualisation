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

## Algorithms:

### Dijkstra:

### Bi-Dijkstra:

### A* Search: