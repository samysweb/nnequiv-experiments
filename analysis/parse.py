import fileinput
import json
import re
from ast import literal_eval

import numpy as np

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
            self.valid_depth=self.parseList(line[14:])
        if line.startswith("[INVALID_DEPTH]"):
            self.invalid_depth=self.parseList(line[16:])
    def parseList(self, str):
        rv = []
        strcache=""
        active=False
        for x in str:
            if x=='[':
                active=True
            elif active:
                if x.isdigit():
                    strcache+=x
                elif x==',' and len(strcache)>0:
                    rv.append(int(strcache))
                    strcache=""
        return np.array(rv)

class ExactCounterLine(LineHandler):
    def __init__(self, run):
        super().__init__("exact_counter", run)
        self.exact_counter_results = None

    def handle(self,line):
        if line.startswith("[EXACT_COUNTERS]"):
            print("Handling ExactCounterLine (may take some time)",flush=True)
            self.exact_counter_results=self.parseList(line[17:])
    
    def parseList(self, str):
        rv = []
        tuplecache=[]
        strcache=""
        active=False
        for x in str:
            if x=='[':
                active=True
            elif active:
                if x.isdigit():
                    strcache+=x
                elif x==',' and len(strcache)>0:
                    tuplecache.append(int(strcache))
                    strcache=""
                elif x==')':
                    tuplecache.append(int(strcache))
                    rv.append((tuplecache[0],tuplecache[1], tuplecache[2]))
                    strcache=""
                    tuplecache=[]
        return np.array(rv)

class DepthOffsetLine(LineHandler):
    def __init__(self,run):
        super().__init__("depth_offset",run)
        self.valid_depth=[]
        self.invalid_depth=[]

    def handle(self,line):
        if line.startswith("[VALID_DEPTH_DECISION]"):
            print("Handling depth_offset (may take some time)",flush=True)
            self.valid_depth=self.parseList(line[23:])
        if line.startswith("[INVALID_DEPTH_DECISION]"):
            print("Handling depth_offset (may take some time)",flush=True)
            print(line[24:100])
            self.invalid_depth=self.parseList(line[25:])
    def parseList(self, str):
        rv = []
        tuplecache=[]
        strcache=""
        active=False
        for x in str:
            if x=='[':
                active=True
            elif active:
                if x.isdigit() or x=='.':
                    strcache+=x
                elif x==',' and len(strcache)>0:
                    tuplecache.append(float(strcache))
                    strcache=""
                elif x==')':
                    tuplecache.append(int(strcache))
                    rv.append((tuplecache[0],tuplecache[1]))
                    strcache=""
                    tuplecache=[]
        return np.array(rv)
                
        

class EquivLine(LineHandler):
    def __init__(self,run):
        super().__init__("equiv",run)
        self.equiv=[]
        self.nonequiv=[]

    def handle(self,line):
        if line.startswith("[EQUIV]"):
            try:
                self.equiv.append(float(line[8:]))
            except ValueError:
                pass
        if line.startswith("[NEQUIV]"):
            self.nonequiv.append(float(line[9:]))

class EquivSummarizesLine(LineHandler):
    def __init__(self,run):
        super().__init__("equiv_summarization",run)
        self.summarized=[]

    def handle(self,line):
        if line.startswith("[EQUIV_SUMMARIZES]"):
            try:
                self.summarized.append(int(line[19:]))
            except ValueError:
                pass

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
    OUT_HANDLERS = [DepthLine, EquivLine, DepthOffsetLine]
    ERR_HANDLERS = [RunLim]
    def __init__(self, stdout, stderr, out_handlers=OUT_HANDLERS, err_handlers=ERR_HANDLERS):
        self.stdout_handlers = []
        self.stderr_handlers = []
        for h in out_handlers:
            self.stdout_handlers.append(h(self))
        for h in err_handlers:
            self.stderr_handlers.append(h(self))
        self.process(stdout,self.stdout_handlers)
        self.process(stderr,self.stderr_handlers)
    
    def process(self, file, handlers):
        with open(file,"r") as f:
            for line in f:
                trueline = line.strip()
                for h in handlers:
                    h.handle(trueline)
