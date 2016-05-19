"""
Threads module.

Common functions and decorators for threading in the project.
"""
import threading


def threadsafe_function(fn):
    """make sure that the decorated function is thread safe."""
    lock = threading.Lock()

    def new(*args, **kwargs):
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()
        return r
    return new

""" Example :
class X:
    var = 0
    @threadsafe_function
    def inc_var(self):
        X.var += 1
        return X.var
"""
