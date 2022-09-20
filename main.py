import mesa


class VacuumCleanerAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        print("Agent No.", self.unique_id, "@:", self.pos)
        self.move()


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

    def step(self):
        self.schedule.step()


model = VacuumCleanerModel(3)
for i in range(10):
    model.step()
