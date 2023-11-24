# Page Simulator
Os Project using page replacement

Submitted by: 22BRS1006 - NAGA RITHESH & 22BRS1147 -SP ROOPESH MATHAV



The management of virtual memory is a critical aspect of modern computer operating systems, allowing programs to exceed the physical memory capacity by utilizing disk storage as an extension. Page replacement algorithms play a pivotal role in optimizing memory usage and minimizing page faults, thereby enhancing overall system performance. This project explores the implementation and simulation of three prominent page replacement algorithms—LRU (Least Recently Used), FIFO (First-In-First-Out), and Optimal—using the psutil and pandas libraries in Python.

The code utilizes psutil to monitor and gather information about running processes, focusing on details such as process ID, CPU usage, memory usage, and more. Three page replacement algorithms are implemented to simulate the eviction and replacement of pages in memory, providing insights into their effectiveness in managing virtual memory. The algorithms are assessed based on their impact on overall system performance and memory utilization.

Key concepts covered in the project include process monitoring, data analysis with pandas, datetime manipulation for timestamp handling, and the use of classes and objects to encapsulate functionality. The PageReplacementSimulator class orchestrates the simulation, tracking page replacement history and providing methods to display process information and recent replacement actions.

The project concludes by demonstrating the effectiveness of the implemented algorithms in optimizing memory usage and minimizing page faults. The combination of psutil, pandas, and simulation techniques offers a comprehensive understanding of page replacement strategies and their implications on system performance



Import modules:
psutil
pandas
collections
