from trackhhl.hamiltonians.simple_hamiltonian import SimpleHamiltonian
from trackhhl.toy.simple_generator import SimpleDetectorGeometry, SimpleGenerator
import numpy as np


def test_SimpleHamiltonian():
    # Generate a test event
    N_DETECTORS = 25
    N_PARTICLES = 50
    detector = SimpleDetectorGeometry([i for i in range(N_DETECTORS)], [10000 for i in range(N_DETECTORS)], [10000 for i in range(N_DETECTORS)], [i+1 for i in range(N_DETECTORS)])
    generator = SimpleGenerator(detector,theta_max=np.pi/3)
    
    event = generator.generate_event(N_PARTICLES)
    
    
    # Initialise Hamiltonian
    EPSILON = 1e-5
    GAMMA = 2.0
    DELTA = 1.0
    
    
    ham = SimpleHamiltonian(EPSILON, GAMMA, DELTA)
    ham.construct_hamiltonian(event)
    sol = ham.solve_classicaly()

    THRESHOLD = .45
    
    discretised_solution = (sol > THRESHOLD)
    truth_solution = [seg.hit_from.track_id == seg.hit_to.track_id for seg in ham.segments]
    
    missed = (discretised_solution != truth_solution).sum()
    print(sol)
    assert missed < .01*len(sol)
    

    