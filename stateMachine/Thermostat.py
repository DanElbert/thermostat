from __future__ import with_statement
import time
import threading

class StateManager(object):
    
    __managerLock = threadingLock()
    
    def __init__(self, startingState, loopDelay):
        self.currentState = startingState
        self.loopDelay = loopDelay
        
    def __setcurrentState(self, value):
        with __managerLock:
            if self._currentState != value:
                self.__currentState = value
                self.__currentState.Entry()
    
    def __getcurrentState(self):
        with __managerLock:
            return self.__currentState
    
    currentState = property(__getcurrentState, __setcurrentState)
    
    def __setisRunning(self, value):
        with __managerLock:
            self.__isRunning = value
            
    def __getisRunning(self):
        with __managerLock:
            return self.__isRunning
        
    isRunning = property(__getisRunning, __setisRunning)
    
    def run(self):
        while self.isRunning:
            self.currentState = self.currentState.EnsureState()
            time.sleep(self.loopDelay)