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

    class HashableArg:
        def __init__(self, arg):
            self.__arg = arg
            try:
                hash(arg)
                self.__hash__ = arg.__hash__
            except TypeError:
                pass

        def __hash__(self):
            return 1

        def __eq__(self, other):
            return self.__arg == other

    # Some arguments may not be hashable,
    # so we wrap them with hashable object 
    def makeArgsHashable(args):
        hashArgs = []
        for arg in args:
            hashArgs.append(HashableArg(arg))
        return hashArgs

    cache = {}

    # Inner function of decorator, takes care of caching function results and
    # freeing memory from old caches
    def inner(*args):
        try:
            cachedCall = cache.get(tuple(args))
        except TypeError as e:
            if 'unhashable' in e.args[0]:
                hashArgs = makeArgsHashable(args)
                cachedCall = cache.get(tuple(hashArgs))
            else:
                # rethrow exception
                raise

        if cachedCall != None and cachedCall.isValid(): 
            result = cachedCall.getResult()
        else:
            result = fn(*args)
    
            cache[tuple(hashArgs)] = FunctionCall(result)
        
        #free invalid caches from memory
        for k,v in list(cache.items()):
            if not v.isValid():
                del cache[k]

        return result
    
    return inner

# TEST
#
#@cacheDecorator
#def log(arg1, arg2):
#    print(arg1, arg2)
#    return time.time()
#
#print(log([1,2,3], "python"))
#time.sleep(0.1)
#print(log([1,2,3], "java"))
#time.sleep(0.1)
#print(log([1,2,3,4], "java"))
#time.sleep(0.1)
#print(log([1,2,3], "python"))
