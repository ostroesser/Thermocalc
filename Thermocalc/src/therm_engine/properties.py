"""
properties is a physical quantities representation and management module

Wikipedia :

A physical quantity (or "physical magnitude") is a physical property 
of a phenomenon, body, or substance, that can be quantified by 
measurement.

@author: Olivier Stroesser
"""

class PhysicalQuantity(object):
    """"
    Represents a physical quantity, which has the main following properties :
        -Value
        -Unit
   """


    def __init__(self, value, unit):
        """
        Constructor
        """
        self.value = value
        self.unit = unit

    def __repr__(self, *args, **kwargs):
        return '{} {}'.format(str(self.value).ljust(15), self.unit.ljust(10))
    
class TemperatureDependentProperty(PhysicalQuantity):
    """
    Represents a property of which the value depends on temperature
    (ex: specific gas heat, liquid viscosity, etc. - a lot of them !)
    
    They are correlated via several formulations, more or less exotic
    
    """
    
    def __init__(self, unit, formulation_code=100):
        self.value = '-'
        self.unit = unit
        self.formulation_code = formulation_code
   
