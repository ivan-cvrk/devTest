import time

def cacheDecorator(fn):
    CACHE_TIME_SECONDS = 5 * 60
    CACHE_CALL_COUNT = 10

    # Class representing cached function call
    class FunctionCall:
        def __init__(self, result):
            self.creationTime = time.time()
            self.callCount = 0
            self.result = result

        def isValid(self):
            return (time.time() - self.creationTime) < CACHE_TIME_SECONDS and self.callCount < CACHE_CALL_COUNT

        def getResult(self):
            self.callCount += 1
            return self.result

    
    cache = {}

    # Inner function of decorator, takes care of caching function results and
    # freeing memory from old caches
    def inner(*args):
        cachedCall = cache.get(tuple(*args))
        
        if cachedCall != None and cachedCall.isValid(): 
            result = cachedCall.getResult()
        else:
            result = fn(*args)
            cache[tuple(*args)] = FunctionCall(result)

        #free invalid caches from memory
        for k,v in list(cache.items()):
            if not v.isValid():
                del cache[k]

        return result
    
    return inner
