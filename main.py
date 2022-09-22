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
        self.cost = 0
        self.points = 0

    def move(self):
        self.model.grid.move_agent(self,(1,0) if self.pos == (0,0) else (0,0))
        self.cost = self.cost + 1

    def vacuum(self, spot):
        self.model.grid.remove_agent(spot)
        self.cost = self.cost + 1
        self.points = self.points+1

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
        if not self.model.finish():
            self.move()
            print("CLEAN")
            print("Action: Move")
        print("After step:")
        print("Agent No.", self.unique_id+1, "@:", self.pos)
        print("In this cell:",
              self.model.grid.get_cell_list_contents([self.pos]))
        print("-------------------")


class VacuumCleanerModel(mesa.Model):
    def __init__(self):
        self.num_agents = 1
        self.grid = mesa.space.MultiGrid(2, 1, True)
        self.schedule = mesa.time.RandomActivation(self)
        a = VacuumCleanerAgent(0, self)
        self.schedule.add(a)
        x = self.random.randrange(self.grid.width)
        self.grid.place_agent(a, (x, 0))
            #Random
        self.grid.place_agent(Dirt(50, DirtModel()), (r.randint(0,1),0))

    def step(self):
        self.schedule.step()

    def finish(self):
        objects = self.grid.get_neighbors((0, 0), moore=True)
        return not any(isinstance(x, Dirt) for x in objects)


model = VacuumCleanerModel()
while not model.finish():
    model.step()
