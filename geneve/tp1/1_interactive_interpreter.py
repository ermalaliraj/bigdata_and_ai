# displays the star only when the elements start with "wh", and print a dash (-) otherwise.

w = ['how', 'why', 'however', 'where', 'never']

for m in w:
    print("*", m[:2], m)

# Should print
# * ho how
# * wh why
# * ho however
# * wh where
# * ne never

print("***Now***")
for m in w:
    if m[:2] == 'wh':
        print("*", m[:2], m)
    else:
        print("-", m[:2], m)

# Should print
# - ho how
# * wh why
# - ho however
# * wh where
# - ne never