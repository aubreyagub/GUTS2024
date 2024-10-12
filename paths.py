from enums import BuildingName
bo_to_lib = [(55.873498, -4.292804), 
                (55.873311, -4.293180), 
                (55.873010, -4.292456),
                (55.872712, -4.291050), 
                (55.872530, -4.289391),
                (55.872807, -4.288762),
                (55.873128, -4.288531),
                (55.873323, -4.288474)]

lib_to_rr = [(55.873323, -4.288474), 
                (55.873102, -4.288537), 
                (55.873065, -4.288317), 
                (55.872884, -4.288315), 
                (55.872674, -4.288206), 
                (55.872346, -4.288193)]

rr_to_bo = [(55.872346, -4.288193),
            (55.872452, -4.289079),
            (55.872521, -4.289712),
            (55.872681, -4.290329),
            (55.872889, -4.290934),
            (55.873012, -4.291090),
            (55.873137, -4.291259),
            (55.873302, -4.291524),
            (55.873498, -4.292804)] 

bo_to_fraser = [(55.873498, -4.292804), 
                (55.873311, -4.293180), 
                (55.873010, -4.292456),
                (55.872712, -4.291050), 
                (55.872530, -4.289391),
                (55.872807, -4.288762),
                (55.873128, -4.288531),
                (55.873218, -4.288445)]

lib_to_fraser = [(55.873323, -4.288474),(55.873218, -4.288445)]  

fraser_to_rr =  [(55.873218, -4.288445),
                (55.873102, -4.288537), 
                (55.873065, -4.288317), 
                (55.872884, -4.288315), 
                (55.872674, -4.288206), 
                (55.872346, -4.288193)]

bo_to_jms = [(55.873498, -4.292804), 
             (55.873311, -4.293180),
             (55.873150, -4.292460)]

jms_to_lib = [(55.873150, -4.292460),
            (55.873010, -4.292456),
            (55.872712, -4.291050), 
            (55.872530, -4.289391),
            (55.872807, -4.288762),
            (55.873128, -4.288531),
            (55.873323, -4.288474)]

jms_to_fraser = [(55.873150, -4.292460),
            (55.873010, -4.292456),
            (55.872712, -4.291050), 
            (55.872530, -4.289391),
            (55.872807, -4.288762),
            (55.873128, -4.288531),
            (55.873218, -4.288445)]

rr_to_jms = [(55.872346, -4.288193),
            (55.872452, -4.289079),
            (55.872521, -4.289712),
            (55.872681, -4.290329),
            (55.872889, -4.290934),
            (55.873012, -4.291090),
            (55.873137, -4.291259),
            (55.873150, -4.292460)]

        
paths = {
    (BuildingName.BOYD_ORR, BuildingName.LIBRARY): bo_to_lib,
    (BuildingName.LIBRARY, BuildingName.BOYD_ORR): bo_to_lib[::-1],
    (BuildingName.LIBRARY, BuildingName.READING_ROOM): lib_to_rr,
    (BuildingName.READING_ROOM, BuildingName.LIBRARY): lib_to_rr[::-1],
    (BuildingName.READING_ROOM, BuildingName.BOYD_ORR): rr_to_bo,
    (BuildingName.BOYD_ORR, BuildingName.READING_ROOM): rr_to_bo[::-1],
    (BuildingName.LIBRARY, BuildingName.READING_ROOM): lib_to_fraser,
    (BuildingName.READING_ROOM, BuildingName.LIBRARY): lib_to_fraser[::-1],
    (BuildingName.BOYD_ORR, BuildingName.READING_ROOM): bo_to_fraser,
    (BuildingName.READING_ROOM, BuildingName.BOYD_ORR): bo_to_fraser[::-1],
    (BuildingName.READING_ROOM, BuildingName.READING_ROOM): fraser_to_rr,
    (BuildingName.READING_ROOM, BuildingName.READING_ROOM): fraser_to_rr[::-1],
    (BuildingName.BOYD_ORR, BuildingName.JMS): bo_to_jms,
    (BuildingName.JMS, BuildingName.BOYD_ORR): bo_to_jms[::-1],
    (BuildingName.JMS, BuildingName.LIBRARY): jms_to_lib,
    (BuildingName.LIBRARY, BuildingName.JMS): jms_to_lib[::-1],
    (BuildingName.JMS, BuildingName.READING_ROOM): jms_to_fraser,
    (BuildingName.READING_ROOM, BuildingName.JMS): jms_to_fraser[::-1],
    (BuildingName.READING_ROOM, BuildingName.JMS): rr_to_jms,
    (BuildingName.JMS, BuildingName.READING_ROOM): rr_to_jms[::-1],
    (BuildingName.BOYD_ORR, BuildingName.BOYD_ORR): [(55.873498, -4.292804)],
    (BuildingName.LIBRARY, BuildingName.LIBRARY): [(55.873323, -4.288474)],
    (BuildingName.READING_ROOM, BuildingName.READING_ROOM): [(55.872346, -4.288193)],
    (BuildingName.READING_ROOM, BuildingName.READING_ROOM): [(55.873218, -4.288445)],
    (BuildingName.JMS, BuildingName.JMS): [(55.873150, -4.292460)]
}