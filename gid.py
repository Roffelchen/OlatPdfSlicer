import os, os.path

path = os.getcwd()
folders = []
for task in os.listdir('./'):
    dir = os.path.join(path, task)
    if os.path.isfile(dir):
        continue
    else:
        folders.append(task)
if len(folders) == 0:
    print('Please create a folder and extract a bulk download of a submission there.')
    input()
    quit()

select = ""
for i, name in enumerate(folders):
    select += f'[{i}] {name} '
select += '[c] Cancel'
noChoice = True
print("Please enter the number of a folder containing the contents of a submission archive (i.e. the folders with the group ids as name):")
print(select)
while (noChoice):

    idx = input()
    idx = idx.strip('[')
    idx = idx.strip(']')
    if idx == 'c' or idx == 'C':
        quit()
    if idx.isnumeric():
        idx = int(idx)
    else:
        print('Please select one of the options above by entering the character in the brackets.')
        continue
    if idx < len(folders):
        noChoice = False
        cnt = 0
        with open('gid.txt', 'w') as out:
            for folder in os.listdir(f'./{folders[idx]}/'):
                dir = os.path.join(path, folders[idx], folder)
                if os.path.isfile(dir):
                    continue
                else:
                    cnt += 1
                    out.write(f'{folder}\n')
        print(f'Successfully extracted {cnt} group ids to \'gid.txt\'.')
        input('Ding!')
        quit()
    else:
        print('Please select one of the options above by entering the character in the brackets.')
        continue
