import subprocess
import os
import time
from subprocess import run
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showerror, showinfo


def run(cmd, work_directory):
    completed = subprocess.run(cmd, shell=True, cwd=work_directory)
    return completed


def run_rt_asc(root, source_path_var, destination_path_var, exe_path_var, total_progress_var, progress_var, current_file_var, console_flags):
    source_path = source_path_var.get()
    destination_path = destination_path_var.get()
    exe_path = exe_path_var.get()
    console_flags = console_flags.get()
    for path in [exe_path, source_path, destination_path]:
        if " " in str(path):
            showerror("Error", "String contains a space")
            exit()
    directories = [name for name in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, name))]
    total_progress_step = 100/len(directories)
    total_progress = 0
    for dir in directories:
        zero_folder = '/' + dir + '/' + 'AC16' + '/' + '0' + '/'
        if os.path.isdir(source_path + zero_folder):
            os.makedirs(destination_path + zero_folder, exist_ok=True)
            zero_dirs = [f.path for f in os.scandir(source_path + zero_folder) if f.is_file()]
            progress = 0
            progress_step = 100/len(zero_dirs)
            for raw_file in zero_dirs:
                current_file_var.set(f"Current File: {raw_file}")
                time.sleep(0.02)
                root.update_idletasks()
                RT_cmd = f"{exe_path} {raw_file} {console_flags}"
                RT_info = run(RT_cmd, destination_path + zero_folder)
                progress = progress + progress_step
                progress_var.set(progress)
                time.sleep(0.02)
                root.update_idletasks()
        else:
            showerror("Error", f"{source_path + zero_folder}\n is not a directory. Program will continue")
        one_folder = '/' + dir + '/' + 'AC16' + '/' + '1' + '/'
        if os.path.isdir(source_path + one_folder):
            os.makedirs(destination_path + one_folder, exist_ok=True)
            one_dirs = [f.path for f in os.scandir(source_path + one_folder) if f.is_file()]
            progress = 0
            progress_step = 100/len(one_dirs)
            for raw_file in one_dirs:
                current_file_var.set(f"Current File: {raw_file}")
                time.sleep(0.02)
                root.update_idletasks()
                RT_cmd = f"{exe_path} {raw_file} {console_flags}"
                RT_info = run(RT_cmd, destination_path + one_folder)
                progress = progress + progress_step
                progress_var.set(progress)
                time.sleep(0.02)
                root.update_idletasks()
        else:
            showerror("Error", f"{source_path + one_folder}\n is not a directory. Program will continue")
        print(f"progress:{total_progress}")
        total_progress = total_progress + total_progress_step
        total_progress_var.set(total_progress)
        time.sleep(0.02)
        root.update_idletasks()

def getFolderPath(path_val):
    folder_selected = askdirectory()
    path_val.set(folder_selected)

def getFilePath(path_val):
    file_selected = askopenfilename()
    path_val.set(file_selected)

def getFlagInfo():
    flags_help = Toplevel()
    flags_help.geometry("500x300")
    flag_info_1 = Label(flags_help, text="Switches\n-Dc\n-Gc\n-Hc\n-Lc\n-Nc\n   \n   \n-Pn\n   \n   \n   \n   \n   \n-Qc\n-Rn\n-Sn\n-Tn\n-Vc")
    flag_info_1.grid(row=0, column=0)
    flag_info_1 = Label(flags_help, text="Description\ninclude DT info in log file: Y, +, N or -\noutput Gathered file: Y, +, N or -\noutput trace Header: Y, +, N or -\nLog file output: Y, +, N or -\nfile Name option:\n\t0/A = use Station Name if present, else use Unit ID\n\t1/I = always use Unit ID\noutput Path levels\n\t0 = no additional subdirectories\n\t1 = one subdirectory level:  YYYY_DDD\n\t2 = two subdirectory levels: YYYY_DDD\HH\n\t3 = two subdirectory levels: YYYY_DDD\HH_MM\n\t4 = two subdirectory levels: YYYY_DDD\HH_MM_SS\nQCC File output: Y, +, N or -\nsample Rate (if not found in the data)\nSample count per channel per event\nTrash n samples from each event\nVerbose message output: Y, +, N or -")
    flag_info_1.grid(row=0, column=1)
    flag_info_1 = Label(flags_help, text="Default\n(NO)\n(NO)\n(YES)\n(YES)\n(Auto)\n\n\n(0)\n\n\n\n\n\n(NO)\n(100)\n(4294967295)\n(0)\n(ENABLED)")
    flag_info_1.grid(row=0, column=2)

def main():
    root = Tk()
    root.title("RT_ASC Helper")

    mainframe = ttk.Frame(root, width=800, height=600)

    description_label = Label(root ,text="Select folder containing data and processed destination location (can be same folder)\n e.g. source : C:/RABT/raw_microseismic_data \n e.g. destination : C:/RABT/processed_data \n Recreates file structure in destination \n Expected data structure is [Source]/[timestamp]/AC16/[0 or 1]/ \n flags example -Rn200 -DcY with spaces \n !! FILE PATH CAN NOT HAVE SPACES !!")
    description_label.grid(row=0,column = 1)

    source_path = StringVar()
    source_label = Label(root ,text="Source:")
    source_label.grid(row=1,column = 0)
    source_entry = Entry(root,textvariable=source_path)
    source_entry.grid(row=1,column=1, padx=50, pady=0, ipadx=300)
    source_button = ttk.Button(root, text="Browse Folder", command=partial(getFolderPath, source_path))
    source_button.grid(row=1,column=2)

    destination_path = StringVar()
    destination_label = Label(root ,text="Destination:")
    destination_label.grid(row=2,column = 0)
    destination_entry = Entry(root,textvariable=destination_path)
    destination_entry.grid(row=2,column=1, padx=50, pady=0, ipadx=300)
    source_button = ttk.Button(root, text="Browse Folder", command=partial(getFolderPath, destination_path))
    source_button.grid(row=2,column=2)

    exe_path = StringVar()
    exe_label = Label(root ,text="Exe:")
    exe_label.grid(row=3,column = 0)
    exe_entry = Entry(root,textvariable=exe_path)
    exe_entry.grid(row=3,column=1, padx=50, pady=0, ipadx=300)
    exe_button = ttk.Button(root, text="Browse Folder", command=partial(getFilePath, exe_path))
    exe_button.grid(row=3,column=2)

    console_flags = StringVar()
    flag_label = Label(root ,text="Flags:")
    flag_label.grid(row=4,column = 0)
    flag_entry = Entry(root,textvariable=console_flags)
    flag_entry.grid(row=4,column=1, padx=50, pady=0, ipadx=300)
    flags_button = ttk.Button(root, text="Flag Help!", command=getFlagInfo)
    flags_button.grid(row=4, column=2)

    current_file_var = StringVar()
    current_folder_label = Label(root ,text="Current File: ", textvariable=current_file_var)
    current_folder_label.grid(row=7, column=1)

    folder_progress_label = Label(root ,text="Folder Progress:")
    folder_progress_label.grid(row=8,column = 0)
    progress_var = DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, orient=HORIZONTAL,length=100,  mode='determinate')
    progress_bar.grid(row=8, column=1, ipadx=300)
    total_progress_label = Label(root ,text="Total Progress:")
    total_progress_label.grid(row=9,column = 0)
    total_progress_var = DoubleVar()
    total_progress_bar = ttk.Progressbar(root, variable=total_progress_var, orient=HORIZONTAL,length=100,  mode='determinate')
    total_progress_bar.grid(row=9, column=1, ipadx=300)

    run_button = ttk.Button(root, text="Run",command=partial(run_rt_asc, root, source_path, destination_path, exe_path, total_progress_var, progress_var, current_file_var, console_flags))
    run_button.grid(row=5,column=1)



    root.mainloop()

if __name__ == '__main__':
    main()