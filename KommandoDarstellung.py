from Service import *
from DatenManager import *

student, studiengang = laden()


class View:
    def __init__(self, student, studiengang):
        self.student = student
        self.studiengang = studiengang
    
    def dashboard(self, student):
        return