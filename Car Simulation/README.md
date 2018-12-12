We want our autonomous cars to navigate throughout the cityof Los Angeles. The cars can move North, South, East, or West. The city can be represented in a grid with (x,y) coordinates. There will be some obstacles, such as buildings, road closings, etc. If a car crashes into a building or road closure, SpeedRacer has to pay $100. 
You know the locations of these, and they will not change over time. You also spend $1 for gas each time you move. The cars will start from a given starting parking lot, and will end at another parking lot. When you arrive at your destination parking lot, you will receive $100. 
Your goal is to make the most money over time with the greatest likelihood. Your cars have a faulty turning mechanism, so they have a chance of 
going in a direction other than the one suggested by your model. They will go in the correct direction 70% of the time (10% in each other direction, including along borders)

Used Bellman's equation of Markov Decision Process to pre-determine the expected efficient directions of each car which should be followed to achieve maximum gain. We then simulate the car movement say 10 times using the probablistic approach and then take mean of all the results.