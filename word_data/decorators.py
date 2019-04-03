from time import time
from functools import wraps

def time_tracker(log_fun):
    def _time_tracker(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            start_time = time()

            try:
                result = fn(*args, **kwargs)
            finally:
                elapsed_time = time() - start_time

                #log results
                log_fun({
                    'function_name': fn.__name__,
                    'total_time': elapsed_time,
                })
            return result

        return wrapped_fn
    return _time_tracker

def _log(message):
    print('[SimpleTimeTracker] {function_name} {total_time:.3f}'.format(**message))