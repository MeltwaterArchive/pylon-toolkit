from pylon import Analysis

pylon = Analysis("datascience", "334f5cd875d8a4d3722c39f7f773e30a", 'linkedin', 'cd99abbc812f646c77bfd8ddf767a134f0b91e84',
    filter='li.user.member.country == "United States"')

filters = {
    'male': 'li.user.member.gender == "male"',
    'female': 'li.user.member.gender == "female"'
}

batch = pylon.freq_dist_batch_filters('li.user.member.age', 10, filters=filters)
df = batch.run()

print(df)