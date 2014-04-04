'''
system is a thermodynamic system representation

@author: Olivier Stroesser
'''

class ThermodynamicSystem(object):
    '''
    Wikipedia :

    A thermodynamic system is a precisely specified macroscopic region of the
    universe, defined by boundaries or walls of particular natures, together
    with the physical surroundings of that region, which determine processes
    that are allowed to affect the interior of the region, studied using the
    principles of thermodynamics.

    All space in the universe outside the thermodynamic system is known as the
    surroundings, the environment, or a reservoir. A system is separated from
    its surroundings by a boundary, which may be notional or real but, by
    convention, delimits a finite volume. Transfers of work, heat, or matter
    and energy between the system and the surroundings may take place across
    this boundary. A thermodynamic system is classified by the nature of the
    transfers that are allowed to occur across its boundary, or parts of its
    boundary.
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

