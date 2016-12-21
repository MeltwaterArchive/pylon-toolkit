from pylon import Analysis

pylon = Analysis("datascience", "334f5cd875d8a4d3722c39f7f773e30a", 'linkedin', 'cd99abbc812f646c77bfd8ddf767a134f0b91e84')

two_level = pylon.nested_freq_dist('Nested example', 'li.user.member.gender', 2, 'li.user.member.age', 5)
print(two_level.run())

three_level = pylon.nested_freq_dist('Nested example', 'li.user.member.country', 2, 'li.user.member.gender', 2, level3='li.user.member.age', threshold3=5)
print(three_level.run())