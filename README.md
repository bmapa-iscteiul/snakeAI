# snakeAI
A snake AI using NEAT 

Libraries:
    - pygame
    - random
    - math
    - neat (neat-python)
    - numpy
    
Simple snake game developed with the sole purpose to use NEAT algorithm in it.

Fitness function -
    +1 fitness for every clock tick
    +1 fitness for every move towards the fruit
    -2.2 fitness for every move away from the fruit
    +10 fitness for every fruit caught
    
TODOS:
    - improve the fitness function
    - improve the inputs provided, maybe add more
    - make fruit not spawn inside the snakes
    
