standard_gpt = """
Determine the intermediate point between the starting point and the end point to form the path, Make sure that the generated path does not pass through any obstacles, nor is it inside an obstacle.
The obstacles are rectangles,[x1,y1],[x2,y2],[x3,y3],[x4, y4] representing the four coordinates of the rectangle.
Please note that answer me as "Generation path: [[x1, y1], [x2, y2],...".
Here are five examples and one question, please learn the examples and output the Generated path.

Start Point: [24.62,17.17]
Goal Point: [31.79,20.42]
Barriers: [[[13.03,7.4],[28.54,7.4],[28.54,9.4],[13.03,9.4]],[[22.24,8.84],[42.24,8.84],[42.24,10.84],[22.24,10.84]],[[26.66,22.73],[43.3,22.73],[43.3,24.73],[26.66,24.73]],[[28.85,13.85],[30.85,13.85],[30.85,25.37],[28.85,25.37]]]
Generated Path: [[24.62,17.17],[27,12],[31,12],[31.79,20.42]]

Start Point: [5.69,8.59]
Goal Point: [36.92,18.7]
Barriers: [[[24.53,9.39],[43.07,9.39],[43.07,11.39],[24.53,11.39]],[[34.2,17.63],[36.2,17.63],[36.2,27.34],[34.2,27.34]],[[26.77,15.45],[38.45,15.45],[38.45,17.45],[26.77,17.45]],[[22.17,17.18],[33.39,17.18],[33.39,19.18],[22.17,19.18]]]
Generated Path: [[5.69,8.59],[25,14],[40,14],[40,18],[36.92,18.7]]

Start Point: [22.96,16.63]
Goal Point: [46.14,28.11]
Barriers: [[[26.24,14.49],[28.24,14.49],[28.24,25.74],[26.24,25.74]],[[42.18,13.53],[44.18,13.53],[44.18,25.47],[42.18,25.47]],[[31.61,18.35],[45.62,18.35],[45.62,20.35],[31.61,20.35]]]
Generated Path: [[22.96,16.63],[25,27],[46.14,28.11]]

Start Point: [12.13,4.5]
Goal Point: [33.88,20.59]
Barriers: [[[30.92,10.36],[32.92,10.36],[32.92,23.24],[30.92,23.24]],[[17.76,20.92],[29.9,20.92],[29.9,22.92],[17.76,22.92]],[[28.63,12.67],[39.36,12.67],[39.36,14.67],[28.63,14.67]]]
Generated Path: [[12.13,4.5], [30, 10], [34, 10], [40,12], [40,15], [33.88,20.59]]

Start Point: [7.32,27.46]
Goal Point: [21.05,15.81]
Barriers: [[[27.16,9.23],[29.16,9.23],[29.16,20.73],[27.16,20.73]],[[12.94,16.17],[33.53,16.17],[33.53,18.17],[12.94,18.17]],[[19.37,22.55],[29.85,22.55],[29.85,24.55],[19.37,24.55]]]
Generated Path: [[7.32,27.46], [12.5,15.81], [21.05,15.81]]

Start Point: {start}
Goal Point: {goal}
Barriers: {barriers}
Generated Path: 
"""
