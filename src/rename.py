import os

path = ".\\images\\train"


def rename_all_files(path):
    filelist = os.listdir(path)
    count = 0
    for file in filelist:
        print(file)
    for file in filelist:
        Olddir = os.path.join(path, file)
        if os.path.isdir(Olddir):
            rename_all_files(Olddir)
            continue
        filetype = os.path.splitext(file)[1]
        Newdir = os.path.join(path, str(count).zfill(4) + filetype)
        os.rename(Olddir, Newdir)
        count += 1


rename_all_files(path)
