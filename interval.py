import threading

def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
