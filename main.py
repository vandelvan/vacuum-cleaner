import mesa
import random as r



class Dirt(mesa.Agent):
    def __init__(self, unique_id: int, model: "Model") -> None:
        super().__init__(unique_id, model)


class DirtModel(mesa.Model):
    def __init__(self):
        super().__init__()


class VacuumCleanerAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned = 0
        self.steps = 1
        self.score = 0


    def move(self):
        self.model.grid.move_agent(
            self, (1, 0) if self.pos == (0, 0) else (0, 0))
        if(self.pos==(0,0)):
            return "left"
        return "right"

    def vacuum(self, spot):
        self.model.grid.remove_agent(spot)

    def isDirty(self):
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for x in cell:
            if isinstance(x, Dirt):
                return x
        return None

    def step(self):
        
        print("-------------------")
        print("Before step:")
        print("Agent No.", self.unique_id+1, "@:", self.pos)
        print("In this cell:",
              self.model.grid.get_cell_list_contents([self.pos]))
        spot = self.isDirty()
        if spot is not None:
            self.vacuum(spot)
            print("DIRTY")
            print("Action: Vacuum")
            self.cleaned += 1
            self.score +=1
            
            
        if not self.model.finish():
            dir=self.move()
            print("CLEAN")
            print("Action: Move to "+dir)
            self.steps += 1
            self.score -= 1

        print("After step:")
        print("Agent No.", self.unique_id+1, "@:", self.pos)
        print("In this cell:",
              self.model.grid.get_cell_list_contents([self.pos]))
        
        print("Score: "+ str(self.score))
        print("Total succes percentage in this round: ", int(self.cleaned/self.steps*100), "%")
        print("-------------------")


class VacuumCleanerModel(mesa.Model):
    def __init__(self):
        self.steps = 1
        self.grid = mesa.space.MultiGrid(2, 1, True)
        self.schedule = mesa.time.RandomActivation(self)
        a = VacuumCleanerAgent(0, self)
        self.schedule.add(a)
        x = self.random.randrange(self.grid.width)
        self.grid.place_agent(a, (x, 0))
        # Random
        spots = r.randint(0, 2)
        for i in range(spots):
            x = self.random.randrange(self.grid.width)
            cell = self.grid.get_cell_list_contents([(x, 0)])
            prevspot = False
            for j in cell:
                if isinstance(j, Dirt):
                    prevspot = True
            if not prevspot:
                self.grid.place_agent(Dirt(i, DirtModel()), (x, 0))

    def step(self):
        self.schedule.step()

    def finish(self):
        objects = self.grid.get_neighbors((0, 0), moore=True)
        return not any(isinstance(x, Dirt) for x in objects)


model = VacuumCleanerModel()
while not model.finish():
    model.step()

print("Press ENTER to close")
input()
