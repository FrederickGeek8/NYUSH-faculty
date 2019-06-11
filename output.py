selected = ["Computer Science", "Data Science", "Interactive Media Arts"]
emails = set()
for disc in selected:
    f = open(disc, "r")
    for line in f:
        data = line.strip().split("\t")
        emails.add(data[1])

print(" ".join(emails))