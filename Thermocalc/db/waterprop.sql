SELECT DISTINCT therm_db.constantproperty.name
        FROM therm_db.substanceconstproperties
        JOIN therm_db.substance on 
            therm_db.substanceconstproperties.id_substance = 
            therm_db.substance.id_substance
        JOIN therm_db.constantproperty on 
            therm_db.substanceconstproperties.id_constant_property = 
            therm_db.constantproperty.id_constant_property
        WHERE therm_db.substance.id_substance = 1