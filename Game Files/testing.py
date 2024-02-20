class Car:
    def __init__(self, color, pos, model=""):
        super().__init__()
        self.color = color
        self.pos = pos
        self.model = model
        
    def get(self):
        if self.model == "":
            self.model = "Model Unknown"
        
        else:
            model = self.model
            self.model = model
        
        print("")
        print(f"[{self.color}, {self.pos}, {self.model}]")
        print("")
            

car1 = Car("Red", 3)
car2 = Car("Blue", 3, model=1980)
