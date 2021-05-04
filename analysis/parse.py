import fileinput
import json
import re

class LineHandler:
    def __init__(self,name,run):
        super().__init__()
        setattr(run,name,self)

    def handle(self, line):
        pass

class DepthLine(LineHandler):
    def __init__(self,run):
        super().__init__("depth",run)
        self.valid_depth=[]
        self.invalid_depth=[]

    def handle(self,line):
        if line.startswith("[VALID_DEPTH]"):
            self.valid_depth=json.loads(line[14:])
        if line.startswith("[INVALID_DEPTH]"):
            self.invalid_depth=json.loads(line[16:])
        

class EquivLine(LineHandler):
    def __init__(self,run):
        super().__init__("equiv",run)
        self.equiv=[]
        self.nonequiv=[]

    def handle(self,line):
        if line.startswith("[EQUIV]"):
            self.equiv.append(float(line[8:]))
        if line.startswith("[NEQUIV]"):
            self.nonequiv.append(float(line[9:]))

class RunLim(LineHandler):
    def __init__(self,run):
        super().__init__("runlim",run)
        self.real=None
        self.time=None
        self.space=None
        self.status=None
    
    def handle(self,line):
        if not line.startswith("[runlim]"):
            return
        content = line[9:]
        parts = re.split('\s+', content)
        try:
            if content.startswith("real:"):
                self.real=float(parts[1])
            elif content.startswith("time:"):
                self.time=float(parts[1])
            elif content.startswith("space:"):
                self.space=float(parts[1])
            elif content.startswith("status:"):
                self.status=parts[1]
        except Exception:
            print("Could not parse "+content+" - parts: "+str(parts))

        

class BenchmarkRun:
    OUT_HANDLERS = [DepthLine, EquivLine]
    ERR_HANDLERS = [RunLim]
    def __init__(self, stdout, stderr):
        self.stdout_handlers = []
        self.stderr_handlers = []
        for h in BenchmarkRun.OUT_HANDLERS:
            self.stdout_handlers.append(h(self))
        for h in BenchmarkRun.ERR_HANDLERS:
            self.stderr_handlers.append(h(self))
        self.process(stdout,self.stdout_handlers)
        self.process(stderr,self.stderr_handlers)
    
    def process(self, file, handlers):
        with open(file,"r") as f:
            for line in f:
                trueline = line.strip()
                for h in handlers:
                    h.handle(trueline)
