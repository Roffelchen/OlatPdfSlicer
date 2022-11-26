import os, os.path
import shutil
import PyPDF2

if os.path.exists('./temp'):
    shutil.rmtree('./temp/')
os.makedirs('./temp')

for file in os.listdir('./'):
    if '.pdf' in file:
        task = file.strip('.pdf')
        if (os.path.exists(f'./{task}_toZip')):
            print(f'Task {task} already split. Skipping...')
            continue
        reader = PyPDF2.PdfReader(file)
        pages = {}
        with open(f'{task}_track.txt') as f:
            for line in f.readlines():
                line = line.split(' ')
                pages[line[0]] = (line[1],line[2])
        for count, key in enumerate(pages):
            print('Document %i of %i' % (count+1, len(pages)), end = "\r")
            os.makedirs(f'./temp/{key}')
            writer = PyPDF2.PdfWriter()
            for i in range(int(pages[key][0])):
                writer.addPage(reader.getPage(int(pages[key][1])+i-1))
            with open(f'./temp/{key}/{task}_Korrektur.pdf', 'wb') as out:
                writer.write(out)
        print()
        with open('./usermap.csv') as um:
            lines = um.readlines()
            if len(lines) > 1:
                map = {}
                for line in lines:
                    (val, key) = line.split(';')
                    key = key.strip()
                    if key in map:
                        map[key].append(val)
                    else:
                        map[key] = [val]
                for count, folder in enumerate(os.listdir(f'./temp/')):
                    print('Group %i of %i' % (count+1, len(os.listdir(f'./temp/'))), end = "\r")
                    if folder in map:
                        for user in map[folder]:
                            os.makedirs(f'./{task}_toZip/{user}')
                            shutil.copy(f'./temp/{folder}/{task}_Korrektur.pdf', f'./{task}_toZip/{user}/')
                os.rename('./temp', f'./{task}_Groups_toZip')
            else:
                print('usermap.csv empty, assuming individual assignment.')
                os.rename('./temp', f'./{task}_toZip')

if os.path.exists('./temp'):
    shutil.rmtree('./temp/')

print()

input('Ding!')
