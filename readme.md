# CSUF Campus Navigation App

![Screenshot 2024-11-05 233554](https://github.com/user-attachments/assets/c931466b-17db-4198-9da1-4d686cc5bbee)

## Live Demo : https://www.linkedin.com/posts/greyson-kim_csuf-csdept-algorithmengineering-activity-7259999102828969984-rvqe?utm_source=share&utm_medium=member_desktop

## Project Overview
This project is a campus navigation application for California State University Fullerton (CSUF), developed as part of CPSC 335. The application utilizes three advanced graph algorithms: Breadth First Search (BFS), Depth First Search (DFS), and Dijkstra's Algorithm to help users find optimal routes across campus. The app is built using Python with `tkinter` for the user interface and `networkx` for graph representation.

## Features
- **Graph Algorithms**: The app demonstrates three powerful algorithms:
  - **Breadth First Search (BFS)**: Explores nodes layer by layer, ideal for unweighted graph traversal.
  - **Depth First Search (DFS)**: Explores nodes deeply along each branch before backtracking, useful for thorough route exploration.
  - **Dijkstra's Algorithm**: Finds the shortest path considering edge weights, optimal for weighted graphs.

- **User Interaction**: Users can:
  - Select start and end nodes.
  - Block specific nodes to simulate route closures.
  - Visualize the pathfinding results of different algorithms.

## Technologies Used
- **Python**: Core programming language.
- **tkinter**: For creating the graphical user interface.
- **networkx**: For graph creation, management, and running pathfinding algorithms.
- **Pillow (PIL)**: To handle the campus map image used in the application.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/username/csuf-campus-navigation.git
   ```
2. Install required packages:
   ```sh
   pip install networkx Pillow
   ```
3. Run the application:
   ```sh
   python main.py
   ```

## Usage
- Launch the application and use the dropdowns to select the start and end points.
- Choose the desired algorithm to visualize the route.
- Use the interface to block nodes and see how the algorithms adapt.

## Project Structure
- **main.py**: Main application file.
- **/images**: Contains the CSUF campus map.
- **/utils**: Utility functions for handling graph operations.

## Challenges and Learnings
- **Node Placement**: Accurately placing nodes on the map based on real campus locations was challenging.
- **Algorithm Visualization**: Effectively visualizing the differences between BFS, DFS, and Dijkstra's required careful design.

## Future Improvements
- Add more campus features like building details and points of interest.
- Implement real-time GPS integration for live navigation.
- Expand the user interface with additional customization options.

## License
This project is licensed under the GNU General Public License (GPL). The code cannot be used or modified by others without explicit permission.

## Acknowledgements
- CSUF CPSC 335 course materials
- [NetworkX Documentation](https://networkx.github.io/)
- [Python tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

## Contact
If you have any questions, feel free to reach out:
- **Minjae Kim** - [LinkedIn](https://linkedin.com/in/greysonkim98)
