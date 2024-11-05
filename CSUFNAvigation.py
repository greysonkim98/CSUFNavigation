import tkinter as tk
from tkinter import ttk
import networkx as nx
import math
from PIL import Image, ImageTk
import random
import threading

class CampusNavigationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CSUF Campus Navigation")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        # Create a graph
        self.G = nx.Graph()

        # Load the campus map image
        self.load_map_image()

        # Original node positions based on the uploaded map dimensions
        # (8439 x 13492 pixels)
        self.node_positions = {
            'A': (110, 140),
            'G': (220, 75),
            'TS': (200, 160),
            'GF': (270, 145),
            'AF': (285, 195),
            'A South': (105, 240),
            'TTF': (235, 245),
            'TSF': (310, 240),
            'CY': (90, 300),
            'D': (160, 315),
            'TTC': (200, 315),
            'IF': (240, 315),
            'EP': (280, 315),
            'H lot': (350, 325),
            'J': (385, 315),
            'RH': (420, 340),
            'SCPS': (125, 370),
            'SRC': (160, 370),
            'TG': (240, 370),
            'SHCC': (320, 380),
            'GAS': (420, 365),
            'TSU': (120, 440),
            'B': (200, 440),
            'PL': (270, 460),
            'EC': (310, 471),
            'E': (370, 410),
            'CS': (395, 410),
            'I': (380, 460),
            'Resident Lot2': (435, 445),
            'TH': (50, 500),
            'VA': (95, 495),
            'CPAC': (200, 520),
            'Quad': (270, 520),
            'H': (320, 520),
            'F': (380, 520),
            'ENPS': (435, 485),
            'ESPS': (435, 525),
            'NPS': (123, 595),
            'C West': (105, 630),
            'C East': (185, 623),
            'MH': (255, 555),
            'CC': (190, 555),
            'DBH': (235, 590),
            'LH': (310, 600),
            'GH': (325, 560),
            'CJ': (335, 570),
            'SGMH': (340, 620),
            'Fullerton Mariott': (420, 610),
            'CP North': (360, 660),
            'CP': (345, 680),
            'CP South': (355, 700),
            'S': (350, 750)
        }

        # Add nodes
        for node, pos in self.node_positions.items():
            self.G.add_node(node, pos=pos)

        # Add edges between adjacent nodes only
        adjacency_list = {
            'A': ['A South', 'G', 'TS'],
            'G': ['A', 'TS', 'GF'],
            'TS': ['A', 'G', 'AF', 'GF'],
            'GF': ['G', 'AF', 'TS'],
            'AF': ['TS', 'GF', 'TTF', 'TSF'],
            'A South': ['A', 'CY', 'D', 'TTF'],
            'TTF': ['TS', 'AF', 'TSF', 'D', 'IF', 'TTC'],
            'TSF': ['AF', 'TTF', 'EP', 'H lot'],
            'CY': ['A South', 'D', 'SCPS'],
            'D': ['CY', 'A South', 'TTC', 'SRC'],
            'TTC': ['TTF', 'D', 'IF', 'TG'],
            'IF': ['TTF', 'TTC', 'EP', 'SHCC'],
            'EP': ['TTF', 'IF', 'TSF', 'H lot'],
            'H lot': ['TSF', 'EP', 'J', 'SHCC'],
            'J': ['H lot', 'RH', 'CS', 'E'],
            'RH': ['J', 'GAS'],
            'SCPS': ['CY', 'SRC', 'TSU'],
            'SRC': ['D', 'SCPS', 'TG'],
            'TG': ['SRC', 'TTC', 'SHCC', 'PL'],
            'SHCC': ['TG', 'EP', 'H lot', 'E'],
            'GAS': ['RH', 'CS', 'Resident Lot2'],
            'TSU': ['SCPS', 'B', 'NPS'],
            'B': ['TSU', 'PL', 'CPAC', 'TG', 'SRC'],
            'PL': ['Quad', 'B', 'EC', 'SHCC'],
            'EC': ['PL', 'H', 'I', 'SHCC', 'Quad'],
            'E': ['CS', 'SHCC', 'I', 'EC'],
            'CS': ['E', 'I', 'J', 'Resident Lot2'],
            'I': ['CS', 'E', 'Resident Lot2', 'ENPS'],
            'Resident Lot2': ['GAS', 'CS', 'ENPS', 'ESPS'],
            'TH': ['VA'],
            'VA': ['TH', 'TSU', 'NPS'],
            'CC': ['CPAC', 'NPS', 'MH', 'DBH', 'C East'],
            'CPAC': ['B', 'Quad'],
            'Quad': ['CPAC', 'H', 'F'],
            'F': ['Quad', 'ENPS', 'ESPS', 'GH', 'CJ', 'Fullerton Mariott', 'H'],
            'ENPS': ['F', 'Resident Lot2', 'ESPS'],
            'ESPS': ['ENPS', 'Resident Lot2'],
            'NPS': ['TSU', 'C West', 'C East'],
            'C West': ['C East', 'NPS'],
            'C East': ['C West', 'NPS', 'DBH'],
            'MH': ['Quad', 'PL', 'DBH'],
            'DBH': ['C East', 'MH', 'LH'],
            'LH': ['SGMH', 'CJ', 'GH'],
            'GH': ['LH', 'CJ', 'F'],
            'CJ': ['GH', 'SGMH', 'Fullerton Mariott', 'F'],
            'SGMH': ['C East', 'CJ'],
            'Fullerton Mariott': ['CJ', 'ESPS', 'CP North', 'F'],
            'CP North': ['CP', 'Fullerton Mariott'],
            'CP': ['CP North', 'CP South'],
            'CP South': ['CP', 'S'],
            'S': ['CP South']
        }

        for node, neighbors in adjacency_list.items():
            for neighbor in neighbors:
                if neighbor in self.node_positions:
                    self.G.add_edge(node, neighbor, weight=math.dist(self.node_positions[node], self.node_positions[neighbor]))

        # Variables to store user selections
        self.start_node = tk.StringVar()
        self.end_node = tk.StringVar()
        self.selected_algorithm = tk.StringVar(value="BFS")
        self.blocked_nodes = set()
        self.selection_mode = None  # Can be 'from', 'to', or None

        self.create_widgets()

    def load_map_image(self):
        # Load the image (replace with your image path)
        image_path = "C:\cpsc335\CSUFNavigation\CSUF_map_resized.jpg"
        self.original_image = Image.open(image_path)
        self.resize_image()

    def resize_image(self):
        # Resize image to fit the window
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        if window_width > 1 and window_height > 1:
            self.image = self.original_image.copy()
            self.image.thumbnail((int(window_width), int(window_height)))
            self.photo = ImageTk.PhotoImage(self.image)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for controls
        left_frame = ttk.Frame(main_frame, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # From selection
        ttk.Label(left_frame, text="From:").pack(pady=5)
        from_dropdown = ttk.Combobox(left_frame, textvariable=self.start_node, values=list(self.node_positions.keys()))
        from_dropdown.pack(pady=5)
        ttk.Button(left_frame, text="Select From on Map", command=lambda: self.set_selection_mode('from')).pack(pady=5)

        # To selection
        ttk.Label(left_frame, text="To:").pack(pady=5)
        to_dropdown = ttk.Combobox(left_frame, textvariable=self.end_node, values=list(self.node_positions.keys()))
        to_dropdown.pack(pady=5)
        ttk.Button(left_frame, text="Select To on Map", command=lambda: self.set_selection_mode('to')).pack(pady=5)

        # Algorithm selection
        ttk.Label(left_frame, text="Algorithm:").pack(pady=5)
        algorithm_dropdown = ttk.Combobox(left_frame, textvariable=self.selected_algorithm, values=["BFS", "DFS", "Dijkstra"])
        algorithm_dropdown.pack(pady=5)

        # Block button
        self.block_button = ttk.Button(left_frame, text="Block Node", command=self.toggle_block_mode)
        self.block_button.pack(pady=5)

        # Run button
        ttk.Button(left_frame, text="Run", command=self.run_algorithm).pack(pady=5)

        # Reset button
        ttk.Button(left_frame, text="Reset", command=self.reset_map).pack(pady=5)

        # Info labels
        self.distance_label = ttk.Label(left_frame, text="Distance: ")
        self.distance_label.pack(pady=5)
        self.time_label = ttk.Label(left_frame, text="Time: ")
        self.time_label.pack(pady=5)

        # Text widget to display the node path order
        self.path_display = tk.Text(left_frame, height=10, width=25, state=tk.NORMAL)
        self.path_display.pack(pady=5)

        # Right frame for map
        self.map_frame = ttk.Frame(main_frame)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.map_frame, bg="white")
        self.scrollbar = ttk.Scrollbar(self.map_frame, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas)

        # Configure canvas and scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create a window inside the canvas to contain the scrollable frame
        self.scrollable_window = self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Place the widgets
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel events for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # For Linux (scroll up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # For Linux (scroll down)

        # Now, the scrollable frame is the accessible frame to add widgets
        self.scrollable_frame = scrollable_frame
        self.draw_map()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.master.bind("<Configure>", self.on_window_resize)

    def _on_mousewheel(self, event):
        # Scroll on Windows and macOS
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def set_selection_mode(self, mode):
        self.selection_mode = mode

    def toggle_block_mode(self):
        if self.block_button.cget("text") == "Block Node":
            self.block_button.config(text="Cancel Block")
        else:
            self.block_button.config(text="Block Node")

    def reset_map(self):
        self.start_node.set("")
        self.end_node.set("")
        self.blocked_nodes.clear()
        self.distance_label.config(text="Distance: ")
        self.time_label.config(text="Time: ")
        self.path_display.delete("1.0", tk.END)
        self.path_display.config(state=tk.DISABLED)
        self.draw_map()

    def on_canvas_click(self, event):
        if self.block_button.cget("text") == "Cancel Block":
            for node, pos in self.node_positions.items():
                if math.dist((event.x, event.y), pos) < 20:
                    if node in self.blocked_nodes:
                        self.blocked_nodes.remove(node)
                    else:
                        self.blocked_nodes.add(node)
                    self.draw_map()
                    break
        elif self.selection_mode in ['from', 'to']:
            for node, pos in self.node_positions.items():
                if math.dist((event.x, event.y), pos) < 20:
                    if self.selection_mode == 'from':
                        self.start_node.set(node)
                    else:
                        self.end_node.set(node)
                    self.selection_mode = None
                    self.draw_map()
                    break

    def on_window_resize(self, event):
        self.resize_image()
        self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")  # Clear the canvas

        # Draw the map image
        if hasattr(self, 'photo'):
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Draw edges
        for edge in self.G.edges():
            start = self.node_positions[edge[0]]
            end = self.node_positions[edge[1]]
            self.canvas.create_line(start[0], start[1], end[0], end[1], fill="black", width=2)

        # Draw nodes
        for node, pos in self.node_positions.items():
            if node == self.start_node.get():
                color = "blue"
            elif node == self.end_node.get():
                color = "orange"
            elif node in self.blocked_nodes:
                color = "red"
            else:
                color = "green"
            self.canvas.create_oval(pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10, fill=color, outline="black")
            self.canvas.create_text(pos[0], pos[1] - 20, text=node, font=("Arial", 10, "bold"))

    def bfs_algorithm(self, graph, start, goal):
        visited = set()
        queue = [[start]]
        paths = []
        min_length = float('inf')

        if start == goal:
            return [[start]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in visited or len(path) <= min_length:
                neighbors = list(self.neighbors(node))
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

                    if neighbor == goal:
                        if len(new_path) < min_length:
                            min_length = len(new_path)
                            paths = [new_path]
                        elif len(new_path) == min_length:
                            paths.append(new_path)

                visited.add(node)

        return paths

    def dfs_algorithm(self, graph, start, goal):
        stack = [(start, [start])]
        all_paths = []
        visited = set()

        while stack:
            (vertex, path) = stack.pop()
            if vertex == goal:
                all_paths.append(path)
            else:
                if vertex not in visited:
                    visited.add(vertex)
                    for neighbor in self.neighbors(vertex):
                        if neighbor not in path:
                            stack.append((neighbor, path + [neighbor]))

        return all_paths

    def dfs_algorithm_threaded(self, graph, start, goal):
        # Use a separate thread to run DFS to avoid blocking the UI
        thread = threading.Thread(target=self._run_dfs, args=(graph, start, goal))
        thread.start()

    def _run_dfs(self, graph, start, goal):
        stack = [(start, [start])]
        all_paths = []
        visited = set()

        while stack:
            (vertex, path) = stack.pop()
            if vertex == goal:
                all_paths.append(path)
            else:
                if vertex not in visited:
                    visited.add(vertex)
                    for neighbor in self.neighbors(vertex):
                        if neighbor not in path:
                            stack.append((neighbor, path + [neighbor]))

        self.display_paths_threaded(all_paths)

    def dijkstra_algorithm(self, graph, start, goal):
        shortest_paths = {start: (None, 0)}
        current_node = start
        visited = set()

        while current_node != goal:
            visited.add(current_node)
            destinations = self.neighbors(current_node)
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = graph[current_node][next_node]['weight'] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return None
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        path = path[::-1]
        return [path]

    def neighbors(self, vertex):
        return list(self.G.neighbors(vertex))

    def run_algorithm(self):
        start = self.start_node.get()
        end = self.end_node.get()
        algorithm = self.selected_algorithm.get()

        if not start or not end:
            return

        # Remove blocked nodes from the graph
        H = self.G.copy()
        H.remove_nodes_from(self.blocked_nodes)

        if algorithm == "BFS":
            paths = self.bfs_algorithm(H, start, end)
            self.display_paths_threaded(paths)
        elif algorithm == "DFS":
            self.dfs_algorithm_threaded(H, start, end)
        elif algorithm == "Dijkstra":
            paths = self.dijkstra_algorithm(H, start, end)
            self.display_paths_threaded(paths)

    def display_paths_threaded(self, paths):
        # Use threading to draw paths for better performance
        thread = threading.Thread(target=self._display_paths, args=(paths,))
        thread.start()

    def _display_paths(self, paths):
        if paths:
            colors = ["blue", "orange", "purple", "pink", "cyan", "magenta", "yellow"]
            total_distance = 0
            for i, path in enumerate(paths):
                color = colors[i % len(colors)]
                path_distance = 0
                for j in range(len(path) - 1):
                    start_node = path[j]
                    end_node = path[j + 1]

                    # Check if nodes exist in self.node_positions
                    if start_node in self.node_positions and end_node in self.node_positions:
                        start_pos = self.node_positions[start_node]
                        end_pos = self.node_positions[end_node]
                        self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], fill=color, width=3)
                        path_distance += self.G[start_node][end_node]['weight']
                    else:
                        print(f"Node {start_node} or {end_node} not found in node_positions")

                total_distance += path_distance

            # Display all paths
            self.path_display.config(state=tk.NORMAL)
            self.path_display.delete("1.0", tk.END)
            for idx, path in enumerate(paths):
                self.path_display.insert(tk.END, f"Path {idx + 1}: {' -> '.join(path)}\n")
            self.path_display.config(state=tk.DISABLED)
            

            # Display total distance and estimated time
            walking_speed = 5  # km/h
            total_time = (total_distance / 1000) / walking_speed * 60  # Convert to minutes
            self.distance_label.config(text=f"Distance: {total_distance:.2f} m")
            self.time_label.config(text=f"Time: {total_time:.2f} minutes")

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigationApp(root)
    root.mainloop()
