# N-Body Simulation
Free space N-Body Simulation according to gravitational forces using Euler's method.

## Inspired study
* http://physics.princeton.edu/~fpretori/Nbody/index.htm

* In the study a system with a large mass in the center had been simulated in a very nice way.  
* Additionally, Barnes Hut and Brute Force methods are compared and the complexity of each method and performance results pointed clearly.


## Contribution
 * In this study, we examine a system with no large masses in the center. 
 * Time steps, radius of the system and the masses of the bodies are calibrated to prevent unexpected behaivor of colliding bodies.
 * Code migrated to python3.7.2
 * GUI implemented with tkinter
 * Barnes Hut Algorithm (As a best practice over Brute Force Algorithm)

## Future Work
- [ ] Verlet Method (As an alternative of Euler's method.) 
- [ ] Data I/O and recording system (Correction data will be needed for numerical analysis)
- [ ] Performance loggers (Monitor the time spent in functions scope.)
- [ ] UI improvements (turtle or other GUI lib for python)

## Usage

### Brute Force
```
cd /src
python3 NBodyAnimator.py

```
