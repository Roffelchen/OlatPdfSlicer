# Description
_OlatPdfSlicer_ is a set of scripts to help with correcting exercises submitted in the Learning Management System [OpenOlat](https://olat.vcrp.de/dmz/).
After bulk downloading a task submission from Olat, _OlatPdfSlicer_ will crawl through the folder structure and merge all submissions into one PDF to allow for easier grading without having to manage multiple files. The PDF is bookmarked with the corresponding username or group id and includes a margin to add notes.
Once corrected, _OlatPdfSlicer_ will recreate the original folder structure to allow for bulk upload on the Olat platform.
This assumes all submissions to be provided in a single PDF file.
# Requirements
The machine executing the scripts needs to have any version of [Python3](https://www.python.org/downloads/) installed (confirmed up to `v3.10.7`), as well as the PDF module [PyPDF2](https://pypdf2.readthedocs.io/en/latest/index.html), which is the only library that needs manual installation. If Python3 is already correctly installed, this is done easiest by running `pip install PyPDF2` in the operating system's native execution shell. _PyPDF2_ is still in development, but the current scripts are confirmed to work with `PyPDF2 v2.11.2` In case of future changes to this library that prevent the scripts from functioning correctly, a manual downgrade can be performed via `pip install PyPDF2==2.11.2`.
# One time setup
If the members of the Olat course submit their exercises individually, no further setup is necessary. Yay!

If however, the members submit their solutions as part of a group, information about the group association needs to be provided. This should be provided in the `usermap.csv` file in the working directory. Initially, this file only contains one line, indicating the format of the data. This information is provided by Olat via the 'Members management' option in the 'Administration' menu (Owner access required).
The .csv should contain one line per member consisting of the Olat username and the group id, separated by a semi-colon (`;`).
Unfortunately, Olat doesn't provide a spreadsheet download with this exact information, so the following downloads and transformations are needed:
1. Download the `TableExport.xlsx` from `Administration -> Members management -> Members`. This includes the full name of the member, and the group _name_ (which is not the same as the group id).
2. Bulk download any submission. Navigate to any 'Task' or 'Group task' course element, select 'Participants', then 'Download all submitted files'. This archive contains two important pieces of information. First, another spreadsheet with a 'Username' to 'First and Last name' map, which together with the file from step 1 can create a 'Username' to 'Group Name' mapping. Second, the subfolders in the archive are labelled with the 'group id' (typically the 'group name' followed by a numeric identifier), with which a 'Username' to 'Group id' map can be created, which can then be entered into the `usermap.csv`. To help extracting the group ids, the helper script `gid.py` (explained below) can be utilized.

Unfortunately (again), Olat only includes a group in the second spreadsheet, if there actually was a submission, so the 'usermap' may be incomplete at first. This, however, is not a problem, since groups without submissions will not get a feedback file anyways.

# Usage
### General Info
* In this section, the term 'cwd' will refer to the 'current working directory', so the folder the scripts are located in.
* To run/execute any of the scripts, double clicking them should be sufficient (provided no other software takes precedence over python when it come to files with the `.py` extension).
Alternatively, navigating to this folder in a terminal and running `python script-name.py` will execute the script. Replace 'script-name' with the corresponding names mentioned below.
* There is no need for additional parameters in the terminal, any potential options are prompted in the console running the script or are achieved by modifying the files in the 'cwd'. These options are explained in the corresponding section for the script.

#### Merging (for grading)
After bulk downloading a submission (see step 2 above), create a folder in the 'cwd' with a name referencing the task. This name will be reused for a lot of purposes, so it should be chosen appropriately (e.g. 'Task 1'). Then, extract the contents of the submission archive into this newly created folder and run the `merge_margin.py` script.
The contents of the created folder are safe, as they are only read.
The script will create a PDF with the same name as the folder in the 'cwd', which can then be opened and edited as any other PDF.
Additionally, a text file with the folder name and '_track' will be created in the 'cwd'. This is **required** to split the graded PDF back into the folder structured required for the bulk upload. Do not edit or remove!
**Note**: As long as this file remains in the 'cwd', another execution of `merge_margin.py` will **not** merge the contents of the folder again, to avoid accidentally overwriting an already graded PDF. If another merge is required, remove the PDF from the folder.
**Note 2**: Since the information about splitting the PDF is stored in the '_track' file, inserting or deleting individual pages in the PDF will lead to incorrect splits, which is why a margin for potential notes is added to the pages in the PDF.
##### Console
* `Ding!`
Successfully executed the merge. Window can be safely closed now.
* `Task $task name$ already merged. Skipping...`
This message indicates that there is already a PDF file with the same name as the folder $task name$. This folder will be skipped to avoid overwriting any changes in the PDF. To execute this script anyways, remove or rename the PDF file.
* `#MORE THAN ONE FILE : $folder name$`
As indicated in the description, these scripts assume submissions of single PDF files. If more than one file was submitted, this message will indicate which user or group has submitted more files. These should be removed and the script rerun.
* `#WRONG FORMAT : $folder name$`
If there was only one file submitted, but it was not a PDF, this message will indicate which user or group submitted the wrong format. This file is ignored, but this way there is an indication that this user or group submitted *something*.
* All other messages (except for exceptions of which there are hopefully none) merely indicate progress.

#### Splitting (for uploading)
With the PDF created in the merging step stored in the 'cwd', running the `split.py` script will have one or more outcomes, depending on whether the `usermap.csv` was filled.
For individual submissions (i.e. the .csv was not changed), a folder with the name of the PDF and '_toZip' is created, containing one folder per username with their respective sections of the graded PDF.
For groups, an additional folder with the ending '_Groups_toZip' is created, containing one folder per group id. Depending on the return structure in Olat, the appropriate folder can be chosen.
As the name implies, the **contents** of these folders (not the folder itself) needs to be packed as a '.zip' archive. So opening the archive displays the folders with the usernames/group ids.
This file can then be uploaded in Olat via the bulk assessment tool found under `Administration -> Bulk assessment (top right corner)`. After selecting the task course element in question, the '.zip' archive can be uploaded and the files will be distributed to the students accordingly.
Optionally, a spreadsheet file can also be uploaded here containing (at least) two columns. One containing the username or group id, the other one(s) containing additional info about the task. Details can be found [here](https://confluence.openolat.org/display/OO153EN/...+create+a+bulk+assessment+for+submission+tasks). A template for this spreadsheet can be created from the already existing spreadsheet in the downloaded submissions folder by removing all columns except for the 'Username' and adding scores/passing status or comments as needed.
##### Console
* `Ding!`
Successfully executed the split. Window can be safely closed now.
* `Task $file name$ already split. Skipping...`
This message indicates that there is already a folder with the same name as the PDF file $file name$. This file will be skipped to avoid overwriting any changes in the folder. To execute this script anyways, remove or rename the PDF file.
* `usermap.csv empty, assuming individual assignment.`
If the `usermap.csv` only contains the template line, the script assumes it was a submission from individual users and no 'Group_toZip' folder will be created.
* All other messages (except for exceptions of which there are hopefully none) merely indicate progress.

#### General usage notes
* Since files/folders that were already handled before are skipped, the 'cwd' can be used for multiple submissions throughout the course. E.g. after handling the first task submissions, another folder (e.g. 'Task 2') can be created and filled with the bulk download of a second task submission and so on. The scripts will indicate which tasks are skipped.
* Changes in group assigments can be handled by editing the `usermap.csv`. This, however, could produce incorrect results, when executing a script with data from previous submissions, which should rarely be necessary, but is mentioned here for completeness anyways.

#### Group ID helper
After bulk downloading a submission and extracting the contents to a folder (see 'Merging' above), run the `gid.py` script. A list of all folders in the 'cwd' is provided and you are prompted to select the one with the extracted submission archive. Selecting the relevant folder is achieved by typing the number of the folder (the one between `[]`). The script will then compile a list of all group ids and save it to `gid.txt`.
When copying the contents of this file and pasting it into any spreadsheet software, you should be prompted whether the content should be split into seperate rows, confirming that will help with creating the map.
