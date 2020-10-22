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

### Dijkstra:

### Bi-Dijkstra:

### A* Search: