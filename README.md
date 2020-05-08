# RLDock

## Fake Landscapes

`fake_landscape.py` has utilities to create quick-to-compute energy landscapes that are meant to loosely model docking landscapes.
You can tune the number of dimensions:

![1D Exmaple](https://raw.githubusercontent.com/JackMaguire/RLDock/master/nevergrad/Figure_1D.png)

![2D Exmaple](https://raw.githubusercontent.com/JackMaguire/RLDock/master/nevergrad/Figure_2D.png)

## Nevergrad Attempt

TODO

## OpenAI Gym / Keras-RL attempt

This was put on the back burner.
The biggest hurdle is that these models appear to only consider the current state of the "game"
and not all of the past states.
