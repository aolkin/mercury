
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
        total = 0
        for i in self.responses:
            if i.get():
                total += 1
                candidates[i.get()] = candidates.get(i.get(),0) + 1
        worst = (float("inf"),None)
        best = (0,None)
        for i, c in candidates.items():
            if c < worst[0]:
                worst = (c,[i])
            elif c == worst[0]:
                worst[1].append(i)
            if c > best[0]:
                best = (c,[i])
            elif c == best[0]:
                best[1].append(i)
        if len(candidates) == 1:
            self.result = worst[1][0]
        elif best[0] > total/2 and len(best[1]) == 1:
            self.result = best[1][0]
            return candidates, best[1]
        elif len(candidates) < 1:
            self.result = True
        else:
            for i in self.responses:
                if i.get() in worst[1]:
                    i.next()
        return candidates, worst[1]


class HighestWins(IteratingResponseCounter):
    class HWResponse(Response):
        def __init__(self, *responses):
            self.responses = responses

        def get(self):
            return self.responses

    response_type = HWResponse

    def step(self):
        candidates = {}
        for res in self.responses:
            for r in res.get():
                candidates[r] = candidates.get(r, 0) + 1
        winners = sorted(list(candidates.items()), key=lambda x: x[1], reverse=True)[:3]
        self.result = list(map(lambda x: x[0], winners))
        return candidates, {x[0]: x[1] for x in winners}



COUNTING_METHODS = {
    0: HighestWins,
    1: IRVQuestion,
    3: HighestWins,
}
