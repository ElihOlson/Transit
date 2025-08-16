# **Transit Code: Real-Time Bus Route Visualizer**

This application is a simple Flask web app that allows users to input their location and view nearby bus routes and stops on an interactive map.
The map is generated using the Folium library and displays location-based transit information. For the backend, we use statistical analysis of historical data to approximate the next arrival time, factoring in travel time.

## **Milestones**
### **Milestone 1**
- Implemented a geolocation detection to display the user's current position on the map in real time
- Use an interactive folium map that helps manipulate the map's visualization and positioning
- Foundation for a more personalized and transit locator experience

### **Milestone 2**
- Load and display bus routes from a bus_route.csv
- Each route is color-coded for easy distinction
- Display bus stops using green bus icons to label each stop with its official stop name.

### **Milestone 3**
- Import and process data from Google Transit Feed Specification (GTFS) files.
  - stop_times.txt – exact arrival and departure times for each stop.
  - trips.txt – mapping between trips and routes.
  - calendar.txt – service schedules.
  - routes.txt – general route descriptions.
  - stops.txt – geolocation and names of stops.
- Parese the mergeed datasets from the Googe Drive historical transit data
- Focus on specific stop_id and route_paths_name even assigning a 1 for each arrival time 
- Apply statistical forecasting models to predict upcoming bus arrival times

### **Milestone 4**
- Implemented bus capacity indicators to inform users of the current capacity status.
  - Most packed routes: 72nd / Ames Avenue, ORBT, 24th Street, Maple Street, Center Street.
  - Peak capacity times: 6:30 AM – 8:00 AM and 4:00 PM – 6:00 PM.
  - If the following bus is at max capacity, the capacity of the next bus will be displayed.
- Added an overall bus capacity status visible in the main window. Which statuses ranged from:
  - Available spaces
  - Limited Space
- Bus capacity statuses include:
  - Open Seating
  - Full, Standing Only
  - Max Capacity
