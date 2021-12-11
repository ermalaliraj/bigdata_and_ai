import lexnlp.extract.en.durations

text = "This Agreement shall terminate ein nine (9) months"
durations = lexnlp.extract.en.durations.get_durations(text)
print("list(durations): ", list(durations))

text = "The period shall not exceed a dozen seconds."
durations = lexnlp.extract.en.durations.get_durations(text)
print("list(durations): ", list(durations))
