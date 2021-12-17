file=open('project.csv','r')
data=file.readlines()
file.close()

durations={}
predecessors={}
schedule={'':(0,0)}

for line in data[1:]:
   line=line.strip().replace('"','')
   line=line.split(',')
   durations[line[0]]=float(line[1])
   predecessors[line[0]]=line[2:]

activities=list(durations.keys())
activities.sort()

for key in activities:
   start_time=0
   for key_pre in predecessors[key]:
       if start_time<schedule[key_pre][1]:
           start_time=schedule[key_pre][1]
   schedule[key]=(start_time,start_time+durations[key])
print(schedule)
