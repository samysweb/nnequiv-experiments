import pandas as pd
import math

class RunlimComparator:
	def __init__(self, run1, run2, benchmarks):
		self.run1 = run1
		self.run2 = run2
		self.benchmarks = benchmarks
	
	def get_data(self):
		data = []
		for b in self.benchmarks:
			cur_row = [None]*9
			cur_row[0]=b
			if self.run1[b] is not None:
				cur_row[1]=self.run1[b].runlim.status
				cur_row[3]=self.run1[b].runlim.real
				cur_row[5]=self.run1[b].runlim.time
				cur_row[7]=self.run1[b].runlim.space
			if self.run2[b] is not None:
				cur_row[2]=self.run2[b].runlim.status
				cur_row[4]=self.run2[b].runlim.real
				cur_row[6]=self.run2[b].runlim.time
				cur_row[8]=self.run2[b].runlim.space
			data.append(cur_row)
		return pd.DataFrame(data, columns=["Name", "Status (1)", "Status (2)", "Real (1)", "Real (2)", "Time (1)", "Time (2)", "Mem (1)", "Mem (2)"])
	
	def render_table(self):
		data = self.get_data()
		def highlight_min(x):
			rv = ['']
			rv.append('color:red' if x[1]!='ok' else '')
			rv.append('color:red' if x[2]!='ok' else '')
			for i in range(2,5):
				if x[2*i] is None or x[2*i-1] is None\
					or math.isnan(x[2*i]) or math.isnan(x[2*i-1]):
					rv.append('')
					rv.append('')
					continue
				if x[2*i]>x[2*i-1]:
					rv.append('font-weight: bold')
					rv.append('')
				else:
					rv.append('')
					rv.append('font-weight: bold')
			return rv
		return data.style.apply(highlight_min,axis=1)

class RunlimMultiComparator:
	def __init__(self, runs, labels, benchmarks):
		self.runs = runs
		self.labels = labels
		self.benchmarks = benchmarks
	
	def get_data(self, attr):
		assert attr in ["status", "real", "time", "space"]
		data = []
		for b in self.benchmarks:
			cur_row = [None]*(len(self.runs)+1)
			cur_row[0]=b
			for i, run in enumerate(self.runs):
				if run[b] is not None:
					cur_row[i+1] = getattr(run[b].runlim, attr)
				else:
					cur_row[i+1] = None
			data.append(cur_row)
		return pd.DataFrame(data, columns=["Name"] + self.labels)
	
	def render_table(self, attr):
		print(f"Table for {attr}")
		data = self.get_data(attr)
		def highlight_min(x):
			rv = ['']
			min_val = min(x[1:])
			for i in range(1,len(x)):
				if x[i]==min_val:
					rv.append('font-weight: bold')
				else:
					rv.append('')
			return rv
		return data.style.apply(highlight_min,axis=1)

class ResultRunlimMultiComparator:
	def __init__(self, runs, labels, benchmarks):
		self.runs = runs
		self.labels = labels
		self.benchmarks = benchmarks
	
	def get_data(self, attr):
		assert attr in ["status", "real", "time", "space"]
		data = []
		for b in self.benchmarks:
			cur_row = [None]*(len(self.runs)+2)
			cur_row[0]=b
			init = False
			equiv = None
			for cur_run in self.runs:
				if init is False and cur_run[b] is not None and cur_run[b].result.did_succeed():
					equiv = cur_run[b].result.is_equiv
					init=True
					continue
				if init\
					and cur_run[b] is not None\
					and cur_run[b].result.did_succeed()\
					and cur_run[b].result.is_equiv != equiv:
					equiv = None
			if equiv is None:
				cur_row[1]="???"
			elif equiv:
				cur_row[1]="equiv"
			else:
				cur_row[1]="not equiv"
			for i, run in enumerate(self.runs):
				if run[b] is not None:
					if not run[b].result.did_succeed():
						cur_row[i+2] = f"fail ({run[b].runlim.status})"
						continue
					cur_row[i+2] = getattr(run[b].runlim, attr)
				else:
					cur_row[i+2] = "???"
			data.append(cur_row)
		return pd.DataFrame(data, columns=["Name", "Status"] + self.labels)
	
	def render_table(self, attr):
		print(f"Table for {attr}")
		data = self.get_data(attr)
		def highlight_min(x):
			rv = ['','']
			min_val = min([val if isinstance(val,float) else float('inf') for val in x[1:]])
			for i in range(2,len(x)):
				if x[i]==min_val:
					rv.append('font-weight: bold')
				else:
					rv.append('')
			return rv
		return data.style.apply(highlight_min,axis=1)