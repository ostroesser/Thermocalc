"""
A chemical substance representation and database operation to manipulate
substances and their properties

@author: Olivier Stroesser
"""

from therm_engine.properties import PhysicalQuantity
from therm_engine.errors import *
import pymysql



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
        SELECT DISTINCT therm_db.constantproperty.name, value, unit
        FROM therm_db.substanceconstproperties
        JOIN therm_db.substance on 
            therm_db.substanceconstproperties.id_substance = 
            therm_db.substance.id_substance
        JOIN therm_db.constantproperty on 
            therm_db.substanceconstproperties.id_constant_property = 
            therm_db.constantproperty.id_constant_property
        WHERE therm_db.substance.id_substance = """ + str(self.id_substance)
                    )
        i=0
        for name, value, unit in cur.fetchall():
            self.properties.append(PhysicalQuantity(value, unit ))
            
            #Binding of a dictionary for easy access to substance properties
            self.property[name] = self.properties[i]
            i += 1
            
        # Disconnect from db
        cur.close()
        conn.close()


def AddDBConstantProperty(id_substance, name, value, unit):
    conn = pymysql.connect(host='127.0.0.1', 
                           port=3306, 
                           user='root', 
                           passwd='drouik', 
                           db='therm_db')
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT therm_db.constantproperty.id_constant_property, 
        therm_db.constantproperty.name
        FROM therm_db.substanceconstproperties
        JOIN therm_db.substance on 
            therm_db.substanceconstproperties.id_substance = 
            therm_db.substance.id_substance
        JOIN therm_db.constantproperty on 
            therm_db.substanceconstproperties.id_constant_property = 
            therm_db.constantproperty.id_constant_property
        WHERE therm_db.substance.id_substance = """ + str(id_substance)
                )
    for prop_id, pname in cur.fetchall():
        if pname == name : # [0] cause pname is a tuple
            update = True
            break
    
    if update:

        cur.execute(""" 
            UPDATE therm_db.constantproperty
            SET value = """ + str(value)+ ", unit = '" + unit +"'\
            WHERE therm_db.constantproperty.id_constant_property = " + 
            str(prop_id))
    else:
        cur.execute("""
            INSERT INTO therm_db.constantproperty (name, value, unit)
            VALUES ('"""+ name + "', " + str(value) + ", '" + unit +"')")
        
        cur.execute("""
            INSERT INTO therm_db.substanceconstproperties 
            (id_substance, id_constant_property)
            VALUES (""" +str(id_substance)+ """, last_insert_id())
            """)

    cur.close()
    conn.commit()
    conn.close()
    
        
if __name__ == '__main__':
    
    try :
        AddDBConstantProperty(1, 'critical_compressibility_factor', 3.2 , '-')
    except DatabaseError as e :
        print('error :', e.value)
    
    try :
        AddDBConstantProperty(1, 'critical_temperature', 3.2 , '-')
    except DatabaseError as e :
        print('error :', e.value)
        
    substance = ChemicalSubstance(1)
    print(substance.property['critical_temperature'])
    print(substance.property['molecular_weight'])