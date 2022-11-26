import PyPDF2
import os, os.path

# Setup

# Iterate through folders
path = os.getcwd()
for task in os.listdir('./'):
    dir = os.path.join(path, task)
    if os.path.isfile(dir):
        continue
    else:
        if f'{task}.pdf' in os.listdir('./'):
            print(f'Task {task} already merged. Skipping...')
            continue
        writer = PyPDF2.PdfWriter()
        totalPages = 0
        track = open(f'{task}_track.txt', 'w')
        print(f'Merging {task}...')
        folder_amount = len(os.listdir(f'./{task}/'))
        for num, folder in enumerate(os.listdir(f'./{task}/')):
            dir = os.path.join(path,task,folder)
            if os.path.isfile(dir):
                continue
            print('Folder %i of %i' % (num+1, folder_amount), end = "\r")
            # Check for multiple files
            if len(os.listdir(f'./{task}/{folder}/1_submissions/')) > 1:
                print(f'#MORE THAN ONE FILE : {folder}')
            file = os.listdir(f'./{task}/{folder}/1_submissions/')[0]
            # Check for file type
            if '.pdf' in file:
                reader = PyPDF2.PdfReader(open(f'./{task}/{folder}/1_submissions/{file}', 'rb'), strict=False)
                track.write(f'{folder} {reader.numPages} {totalPages + 1}\n')
                for i in range(0, reader.numPages):
                    #writer.addPage(reader.getPage(i))
                    curPage = reader.getPage(i)
                    newPage = writer.addBlankPage(
                        curPage.mediaBox.getWidth() + (curPage.mediaBox.getWidth()/3),
                        curPage.mediaBox.getHeight())
                    newPage.mergeScaledPage(curPage, 1)
                    if i == 0:
                        writer.addBookmark(f'{folder}', totalPages, parent=None)
                    totalPages += 1
                #print(file, reader.numPages)
            else:
                print(f'#WRONG FORMAT : {folder}')
        # Print files
        track.close()
        with open(f'./{task}.pdf', 'wb') as out:
            writer.write(out)

print('')
input('Ding!')
