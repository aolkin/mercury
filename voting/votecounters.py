
class Response:
    def __init__(self,response):
        self.response = response
        
    def get(self):
        return self.response

class ResponseCounter:
    response_type = Response

    def __init__(self,responses):
        self.responses = self.prep(responses)

    def prep(self,responses):
        return responses

    def get(self):
        """Must return the final result, an object from the responses
        dictionary."""
        raise NotImplementedError()

class IteratingResponseCounter(ResponseCounter):
    def __init__(self,responses):
        self.responses = self.prep(responses)
        self.result = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.get():
            raise StopIteration
        else:
            return self.step()

    def get(self):
        return self.result

    def step(self):
        """Should perform one iteration of the counting process and
        return intermediate data."""
        raise NotImplementedError()

class IRVQuestion(IteratingResponseCounter):
    class IRVResponse(Response):
        def __init__(self,*responses):
            self.responses = responses
            self.index = 0
    
        def get(self):
            if len(self.responses) > self.index:
                return self.responses[self.index]
            else:
                return None
                
        def next(self):
            self.index += 1

    response_type = IRVResponse

    def step(self):
        candidates = {}
        for i in self.responses:
            if i.get():
                candidates[i.get()] = candidates.get(i.get(),0) + 1
        worst = (float("inf"),None)
        for i, c in candidates.items():
            if c < worst[0]:
                worst = (c,[i])
            elif c == worst[0]:
                worst[1].append(i)
        if len(candidates) == 1:
            self.result = worst[1][0]
        elif len(candidates) < 1:
            self.result = True
        else:
            for i in self.responses:
                if i.get() in worst[1]:
                    i.next()
        return candidates, worst[1]

COUNTING_METHODS = {
    1: IRVQuestion,
}
