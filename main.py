import mesa


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
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
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
        print("Before step:")
        print("Agent No.", self.unique_id, "@:", self.pos)
        print("In this cell:",
              self.model.grid.get_cell_list_contents([self.pos]))
        spot = self.isDirty()
        if spot is not None:
            self.vacuum(spot)
        if not self.model.finish():
            self.move()
        print("After step:")
        print("Agent No.", self.unique_id, "@:", self.pos)
        print("In this cell:",
              self.model.grid.get_cell_list_contents([self.pos]))


class VacuumCleanerModel(mesa.Model):
    def __init__(self, N):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(2, 1, True)
        self.schedule = mesa.time.RandomActivation(self)
        for i in range(self.num_agents):
            a = VacuumCleanerAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            self.grid.place_agent(a, (x, 0))
            self.grid.place_agent(Dirt(50, DirtModel()), (0, 0))

    def step(self):
        self.schedule.step()

    def finish(self):
        objects = self.grid.get_neighbors((0, 0), moore=True)
        return not any(isinstance(x, Dirt) for x in objects)


model = VacuumCleanerModel(1)
while not model.finish():
    model.step()
