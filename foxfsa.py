def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class FoxFSA:
    def __init__(self):
        # initializing states
        self.chases = self._create_chases()
        self.runs = self._create_runs()
        self.eats = self._create_eats()
        self.recovers = self._create_recovers()

        # setting current state of the system
        self.current_state = self.chases

        # stopped flag to denote that iteration is stopped due to bad
        # input against which transition was not defined.
        self.stopped = False

    def get_state(self):
        if self.current_state == self.eats:
            return 'Fox won' # Hegdehog is eaten
        elif self.current_state == self.recovers:
            return 'Fox Recovers' # Fox is beaten and in recovery state
        elif self.stopped:
            return 'Stopped' # due to invalid input
        elif self.current_state == self.runs:
            return 'Running'
        elif self.current_state == self.chases:
            return 'Chasing'

        return 'Undefined state'

    def send(self, event):
        """The function sends the input event to the current state
        It captures the StopIteration exception and marks the stopped flag.
        """
        try:
            self.current_state.send(event)
        except StopIteration:
            self.stopped = True

    @prime
    def _create_chases(self):
        while True:
            # Wait till the input is received.
            string = yield

            # depending on what we received as the input
            # change the current state of the fsm
            if string == 'p': #powermode
                self.current_state = self.runs
            elif string == 'm': #meeting
                self.current_state = self.eats
            elif string == '' or string == 't': #empty
                self.current_state = self.chases
            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break

    @prime
    def _create_runs(self):
        while True:
            # Wait till the input is received.
            string = yield

            # depending on what we received as the input
            # change the current state of the fsm
            if string == 'm': #meeting
                self.current_state = self.recovers
            elif string == '' or string == 'p': #empty
                self.current_state = self.runs
            elif string == 't':
                self.current_state = self.chases
            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break

    @prime
    def _create_eats(self):
        while True:
            # Wait till the input is received.
            string = yield
            print(string)
            break

    @prime
    def _create_recovers(self):
        while True:
            # Wait till the input is received.
            string = yield
            if string == 'm': #meeting
                self.current_state = self.recovers
            elif string == '' or string == 'p': #empty
                self.current_state = self.runs
            elif string == 't':
                self.current_state = self.chases
            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break
