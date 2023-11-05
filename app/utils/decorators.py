import time

ENABLE_TIMER = True
ENABLE_DEBUG = False

class TimingDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if ENABLE_TIMER:
            start_time = time.time()
            result = self.func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f">>> {self.func.__name__} took {elapsed_time:.4f} seconds")
        else:
            result = self.func(*args, **kwargs)
        return result

class DebugDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if ENABLE_DEBUG:
            function_name = self.func.__name__
            input_str = f"Input: args={args}, kwargs={kwargs}"
            start_time = time.time()
            result = self.func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            output_str = f"Output: {result}"
            
            print(f"Function: {function_name}")
            print(input_str)
            print(output_str)
            print(f">>> {function_name} took {elapsed_time:.4f} seconds")
        else:
            result = self.func(*args, **kwargs)
        
        return result