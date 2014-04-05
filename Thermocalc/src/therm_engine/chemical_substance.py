"""
A chemical substance representation and database operation to manipulate
substances and their properties

@author: Olivier Stroesser
"""

import pymysql

from therm_engine.properties import PhysicalQuantity,\
    TemperatureDependentProperty


class ChemicalSubstance(object):
    '''
    Class for substances (water, ethanol, lysergic acid diethylamide...)

    Wikipedia :

    In chemistry, a chemical substance is a form of matter that has constant
    chemical composition and characteristic properties.[1] It cannot be
    separated into components by physical separation methods, i.e. without
    breaking chemical bonds. It can be solid, liquid, gas, or plasma.

    [Well.. liquid or gas would be a good start in this module]
    '''
    

    def __init__(self, id_substance):
        """
        Constructor
        """
        self.name = "SUBSTANCE"
        self.id_substance = id_substance
        self.properties = []
        self.property = {}

        # Connection to MySQL chemical database
        conn = pymysql.connect(host='127.0.0.1',
                               port=3306,
                               user='olivier',
                               passwd='drouik',
                               db='therm_db')
        cur = conn.cursor()
        
        cur.execute("""
            SELECT DISTINCT constantproperty.name, 
            constantproperty.value, constantproperty.unit
            FROM substanceconstproperties
            JOIN substance on substanceconstproperties.id_substance = 
                substance.id_substance
            JOIN constantproperty on 
                substanceconstproperties.id_constant_property = 
                constantproperty.id_constant_property
            WHERE substance.id_substance = {}
            """.format(str(id_substance)))
        i = 0
        for name, value, unit in cur.fetchall():
            self.properties.append(PhysicalQuantity(value, unit))
            # Binding of a dictionary for easy access to substance properties
            self.property[name] = self.properties[i]
            i += 1
        
        cur.execute(""" 
            SELECT DISTINCT tdependentproperty.name, tdependentproperty.unit
            FROM SubstancetDependentProperty
            JOIN substance on SubstancetDependentProperty.id_substance = 
                substance.id_substance
            JOIN tdependentproperty on 
                SubstancetDependentProperty.id_t_dependent_property = 
                tDependentProperty.id_t_dependent_property
            WHERE substance.id_substance = {}
            """.format(str(id_substance)))
        
        for name, unit in cur.fetchall():
            self.properties.append(TemperatureDependentProperty(unit))
            # Binding of a dictionary for easy access to substance properties
            self.property[name] = self.properties[i]
            i += 1
            
        # Disconnect from db
        cur.close()
        conn.close()
    def __repr__(self, *args, **kwargs):
        reprs = self.name.center(80,'=') + "\n"
        for name, prop in substance.property.items() :
            reprs += '{0:35} {1:1}'.format(name, prop)
            reprs += "\n"
        return reprs    

def AddDBProperty(id_substance, name, unit, value='NoValue'):
    """
    Add a property to a substance
    If the 'value' argument is omitted, a temperature-dependent
    property is added
    """
    if value == 'NoValue' :
        # Temperature dependent properties SQL queries
        select_properties = """ 
            SELECT DISTINCT tdependentproperty.id_t_dependent_property, 
            tdependentproperty.name
            FROM SubstancetDependentProperty
            JOIN substance on SubstancetDependentProperty.id_substance = 
                substance.id_substance
            JOIN tdependentproperty on 
                SubstancetDependentProperty.id_t_dependent_property = 
                tDependentProperty.id_t_dependent_property
            WHERE substance.id_substance = {}
            """.format(str(id_substance))
            
        update_properties = """ 
            UPDATE tDependentProperty  
            SET unit = '{}'
            WHERE tDependentProperty.id_t_dependent_property =
            """.format(str(unit))
        
        insert_properties = """
            INSERT INTO tDependentProperty (name, unit)
            VALUES ('{}', '{}');
            INSERT INTO SubstancetDependentProperty 
                (id_substance, id_t_dependent_property)
            VALUES ({}, last_insert_id());
            """.format(name, unit, str(id_substance))
        
    else :
        # constant properties SQL queries
        select_properties = """
            SELECT DISTINCT constantproperty.id_constant_property, 
            constantproperty.name
            FROM substanceconstproperties
            JOIN substance on substanceconstproperties.id_substance = 
                substance.id_substance
            JOIN constantproperty on 
                substanceconstproperties.id_constant_property = 
                constantproperty.id_constant_property
            WHERE substance.id_substance = {}
            """.format(str(id_substance))
        
        update_properties = """ 
            UPDATE constantproperty
            SET value = {}, unit = '{}'
            WHERE constantproperty.id_constant_property = 
            """.format(str(value), unit)
        
        insert_properties = """
            INSERT INTO constantproperty (name, value, unit)
            VALUES ('{}', {}, '{}');
            INSERT INTO substanceconstproperties
            (id_substance, id_constant_property)
            VALUES ({}, last_insert_id());
            """.format(name, str(value), unit, str(id_substance))
        
    update = False
    
    conn = pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           passwd='drouik',
                           db='therm_db')
    cur = conn.cursor()
    cur.execute(select_properties)
    for prop_id, pname in cur.fetchall():
        if pname == name :  # if property already exists
            update = True
            break
    
    if update:
        cur.execute(update_properties + str(prop_id))
    else:

        cur.execute(insert_properties)

    cur.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
#     
    AddDBProperty(1, 'gas_ideal_specific_heat', 'J/mol/K')    
#     AddDBProperty(1, 'van_der_waals_volume', 'm^3/mol', 0.45)
    substance = ChemicalSubstance(1)
    print(substance)
    
    

