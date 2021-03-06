import fileinput
import json
import re
import statistics
from statistics import StatisticsError
from ast import literal_eval

import numpy as np

class LineHandler:
    def __init__(self,name,run):
        super().__init__()
        setattr(run,name,self)

    def handle(self, line):
        pass

    def check(self):
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
        
class CegarOptimal(LineHandler):
    def __init__(self, run):
        super().__init__("cegaropt", run)
        self.cegar=None
        self.opt=None
    def handle(self,line):
        if line.startswith("[CEGAR_TIME]"):
            self.cegar = float(line.split(" ")[-1])
        if line.startswith("[OPTIMAL_TIME]"):
            self.opt = float(line.split(" ")[-1])

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
    
    def check(self):
        if self.real is None or self.time is None or self.space is None or self.status is None:
            print("Did not get all runlim values!")
            raise Exception()

class NNEquivSplitsHandler(LineHandler):
    def __init__(self, run):
        super().__init__("split", run)
        self.split_positions = {}
    
    def handle(self,line):
        if line.startswith('[SPLIT_POINTS]'):
            self.parseList(line[15:])
    
    def parseList(self, str):
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
                    pos = (tuplecache[0],tuplecache[1],tuplecache[2])
                    if pos in self.split_positions:
                        self.split_positions[pos]+=1
                    else:
                        self.split_positions[pos]=1
                    strcache=""
                    tuplecache=[]


class NNEquivResultHandler(LineHandler):
    def __init__(self,run):
        super().__init__("result",run)
        self.status = None
        self.finished = False
        self.is_equiv = True
    
    def did_succeed(self):
        return self.status=="ok" and self.finished
    
    def handle(self,line, out=None):
        assert out is not None
        if out=="stdout":
            if line.startswith('\033[') and "calls" in line:
                # Timer was printed
                self.finished=True
            if line.startswith('[NEQUIV]'):
                self.is_equiv=False
        elif out=="stderr":
            if not line.startswith("[runlim]"):
                return
            content = line[9:]
            parts = re.split('\s+', content)
            if content.startswith("status:"):
                self.status=parts[1].strip()

class BueningResultHandler(LineHandler):
    BOUND_THRESHOLD = 1e-8
    def __init__(self,run):
        super().__init__("result",run)
        self.status = None
        self.is_equiv = True
    
    def did_succeed(self):
        return self.status=="ok"
    
    def handle(self,line, out=None):
        assert out is not None
        if out=="stdout":
            if line.startswith('Best objective '):
                split_line = line.split(",")[0].split(" ")
                bound = float(split_line[2])
                if bound > BueningResultHandler.BOUND_THRESHOLD:
                    self.is_equiv = False
        elif out=="stderr":
            if not line.startswith("[runlim]"):
                return
            content = line[9:]
            parts = re.split('\s+', content)
            if content.startswith("status:"):
                self.status=parts[1].strip()
        

class BenchmarkRun:
    OUT_HANDLERS = [DepthLine, EquivLine, DepthOffsetLine]
    ERR_HANDLERS = [RunLim]
    def __init__(self, stdout, stderr, out_handlers=OUT_HANDLERS, err_handlers=ERR_HANDLERS, both_handlers=[]):
        self.stdout_handlers = []
        self.stderr_handlers = []
        self.both_handlers = []
        for h in out_handlers:
            self.stdout_handlers.append(h(self))
        for h in err_handlers:
            self.stderr_handlers.append(h(self))
        for h in both_handlers:
            self.both_handlers.append(h(self))
        self.process(stdout,self.stdout_handlers, "stdout")
        self.process(stderr,self.stderr_handlers, "stderr")
        for h in self.stdout_handlers:
            h.check()
        for h in self.stderr_handlers:
            h.check()
        for h in self.both_handlers:
            h.check()
    
    def process(self, file, handlers, out):
        with open(file,"r") as f:
            for line in f:
                trueline = line.strip()
                for h in handlers:
                    h.handle(trueline)
                for h in self.both_handlers:
                    h.handle(trueline, out=out)

class AggregateRun:
    def __init__(self, valuelist):
        self.valuelist=valuelist
    
    def get_val(self, attr, strategy='M'):
        results = []
        for val in self.valuelist:
            cached_val = val
            for a in attr:
                cached_val=getattr(cached_val,a)
            results.append(cached_val)
        if strategy=='M':
            try:
                return statistics.median(results)
            except (StatisticsError, TypeError):
                return None
        elif strategy=='A':
            return results