# COP-Population-Dynamics

## How to run

Run main.py to run the animation.

If you don't want to execute from main.py, you need to specify your working directory to be the same as the root folder (```COP-Population-Dynamics```).

### Why is this project structured like this?

We intended to write a general evolution engine that will accept any static (food) and dynamic (animal) objects. This is why the project is structured like a library and is intended to be used by importing ```AnimalEvolution``` from ```population_dynamics.py```. Then you feed it your own food and animals, similar to how we feed it the classes from ```src/animals.py``` in the example ```examples/graphs.py```. 

## Features

- Population model simulation engine.
- Carrots, Rabbits and Foxes as an example.
- Supports evolution of a species.
- Create custom animals or food with custom behaviour and interactions.

## Dependencies

- Numpy
- Matplotlib
- Numba
- PyQt5

## Important files

- ```src/population_dynamics.py``` contains the structure of the playing field.
- ```src/animals``` contains class structure (```Entity```, ```Animal```) and specifically ```Carrot```, ```Rabbit``` and ```Fox```.
- Examples can be found in the examples folder. 
- You can process data using ```src/analysis.py```.