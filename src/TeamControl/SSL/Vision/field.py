import logging

class Field():
    """
    Field data of world Model
    """
    def __init__(self, field_data) -> None:
        self.field_length = field_data.field_length
        self.field_width = field_data.field_width
        self.goal_width = field_data.goal_width
        self.goal_depth = field_data.goal_depth
        self.boundary_width = field_data.boundary_width
        self.lines = list()
        self.extract_field_lines(field_data.field_lines)
        self.extract_field_arc(field_data.field_arcs)
        
    def get_line(self, type_of_line:int):
        # list of constant 
        #working in progress

        w = "Right goal line"
        for item in self.lines:
            if w in item.name:
                print(w)
   
    def extract_field_lines(self, lines):
        for line in lines:
            self.lines.append(Lines(line))
        logging.debug(self.lines)            
        
    
    def extract_field_arc(self, arcs):
        for arc in arcs:
            self.lines.append(Arc(arc))
    
    def __repr__(self) -> str:
        return f'''
    Field Dimension 
    length: {self.field_length} x width: {self.field_width}
    
    Goal Dimension  
    Depth: {self.goal_depth} x width: {self.goal_width}
    
    Boundary width: {self.boundary_width}
    
    lines and arcs:
    {self.lines}
                '''
        
    ### --- END Update Geometry Data --- ### 

class Lines():
    def __init__(self, line_data) -> None:
        self.name = line_data.name
        self.p1 = (int(line_data.p1.x), int(line_data.p1.y))
        self.p2 = (int(line_data.p2.x), int(line_data.p2.y))
        self.length = (self.p2[0] - self.p1[0], self.p2[1] - self.p1[1])
        self.thickness = line_data.thickness
        
    def __repr__(self) -> str:
        return f"\n     Line \033[1m{self.name}\033[0m from {self.p1} to {self.p2}, length : {self.length} thickness : {self.thickness}"

class Arc():
    def __init__(self, arc_data) -> None:
        self.name = arc_data.name
        self.centre = (arc_data.center.x, arc_data.center.y)
        self.radius = arc_data.radius
        self.inner = arc_data.a1
        self.outer = arc_data.a2
        self.area = self.outer - self.inner
        self.thickness = arc_data.thickness
    
    def __repr__(self) -> str:
        return f"\n     arc \033[1m{self.name}\033[0m, centre @ {self.centre}, radius : {self.radius}, area : {self.area}, thickness : {self.thickness}\n"
         