l = [[{'Name': 'Alice', 'Age': 40, 'Point': 80},
     {'Name': 'Bob', 'Age': 20},
     {'Name': 'Charlie', 'Age': 30, 'Point': 10}],
     [{'Name': 'Alice', 'Age': 40, 'Point': 80},
     {'Name': 'Bob', 'Age': 20},
     {'Name': 'Charlie', 'Age': 30, 'Point': 70}],
     [{'Name': 'Alice', 'Age': 40, 'Point': 30},
     {'Name': 'Bob', 'Age': 20},
     {'Name': 'Charlie', 'Age': 30, 'Point': 20}]]
x = sorted(l, key=lambda x: x[2]['Point'])
print(x)