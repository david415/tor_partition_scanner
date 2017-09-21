
class CircuitGeneratorFromFile(object):
    def __init__(self, filepath, torstate):
        self.filepath = filepath
        self.torstate = torstate

        def circuit_generator():
            with open(self.filepath, 'r') as fh:
                for line in fh:
                    fields = line.split("|")
                    assert len(fields) == 2
                    routerA = self.torstate.router_from_id(fields[0])
                    routerB = self.torstate.router_from_id(fields[1])
                    yield [routerA, routerB]

        self._circgen = circuit_generator()

    def next(self):
        return self._circgen.next()
