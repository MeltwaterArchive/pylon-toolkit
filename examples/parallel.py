from pylon import Analysis

pylon = Analysis("datascience", "334f5cd875d8a4d3722c39f7f773e30a", 'linkedin', 'cd99abbc812f646c77bfd8ddf767a134f0b91e84')

task1 = pylon.freq_dist('Interaction types', 'li.type')
task2 = pylon.freq_dist('Interaction types', 'li.subtype')

task1.start()
task2.start()
pylon.waitAll()

print(task1.df())
print(task2.df())