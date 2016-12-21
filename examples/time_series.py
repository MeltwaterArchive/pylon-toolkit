from pylon import Analysis

pylon = Analysis("datascience", "334f5cd875d8a4d3722c39f7f773e30a", 'linkedin', 'cd99abbc812f646c77bfd8ddf767a134f0b91e84')

task = pylon.time_series('ts', 'day')
df = task.run()
print(df)