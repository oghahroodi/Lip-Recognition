import glob
import operator

data_set = '..\\..\\org_data_set\\'


text_file = glob.glob(data_set+'\\*\\*.txt')
count = {}

# print(text_file)
for i in text_file:
    f = open(i, 'r+')
    # print(f.read().split('\n'))
    l = f.read().split('\n')

    for j in range(4, len(l)-1):
        word = l[j].split()[0]
        if word not in count.keys():
            count[word] = 1
        else:
            count[word] += 1
    # break

# print(count)
sorted_count = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_count)
