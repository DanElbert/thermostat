from __future__ import with_statement
import time
import thread

class StateManager(object):
    
    def __init__(self, startingState, loopDelay, logger = None):
        
        self.__managerLock = thread.allocate_lock()
        self.__currentState = None
        
        self.currentState = startingState
        self.loopDelay = float(loopDelay)
        self.stop = False
        self.logger = logger
        
    def __setcurrentState(self, value):
        with self.__managerLock:
            if self.__currentState != value:
                self.__currentState = value
                self.__currentState.Entry()
    
    def __getcurrentState(self):
        with self.__managerLock:
            return self.__currentState
    
    currentState = property(__getcurrentState, __setcurrentState)
    
    def __setstop(self, value):
        with self.__managerLock:
            self.__stop = value
            
    def __getstop(self):
        with self.__managerLock:
            return self.__stop
        
    stop = property(__getstop, __setstop)
    
    def __setlogger(self, value):
        with self.__managerLock:
            self.__logger = value
            
    def __getlogger(self):
        with self.__managerLock:
            return self.__logger
        
    logger = property(__getlogger, __setlogger)
    
    def run(self):
        while not self.stop:
            if self.logger != None:
                self.logger.log(self.currentState)
            self.currentState = self.currentState.UpdateState()
            time.sleep(self.loopDelay)