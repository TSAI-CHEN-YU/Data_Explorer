# import necessary libraries
import pandas as pd
import os, glob, json, sys, openpyxl


print('load...')
# use glob to get all the csv files 
# in the folder

path = sys.argv[1] if len(sys.argv) > 1 else []
files = glob.glob(os.path.join(path, "*.csv"))+glob.glob(os.path.join(path, "*.xlsx"))+glob.glob(os.path.join(path, "*.txt"))+glob.glob(os.path.join(path, "*.pickle"))

# drop mutiple sheet xlsx
files = files + glob.glob(os.path.join(f'{path}/tmp', "*.xlsx"))
for f in files:
    if ".xlsx" in f: 
        # 若包含多個sheet，delete
        wb = openpyxl.load_workbook(f)
        if len(wb.sheetnames)!=1:
            files.remove(f)

# print(files)
files_name = [os.path.basename(i) for i in files]
print(files_name)

# loop over the list of csv files
filename_list, tablecol_list, all_column_list,  = [ [] for x in range(3) ]
json_save_list = []
for f, f_n in zip(files,files_name):
    # file name
    if '.txt' in f:
        df = pd.read_table(f,sep=',') 
    # xlsx
    elif '.xlsx' in f:
        df = pd.read_excel(f,engine='openpyxl')
    # csv
    elif '.csv' in f:
        df = pd.read_csv(f, nrows=1)
    # pickle
    elif '.pickle' in f:
        df = pd.read_pickle(f)
    filename = f_n.split(".")[0]

    # file columns
    colnames = list(df.columns)
    tablecol = [f'{filename}.{i}' for i in colnames]

    # json element
    json_save = dict(label=filename,
                     title=filename,
                     value=filename,
                     children=[dict(label=i,
                                    title=i,
                                    value=f'{filename}.{i}',
                                    description='some description...') for i in colnames]
                    )
    
    json_save_list.append(json_save)
    
# output to  data_table.json
with open("data.json", "w") as outfile:
    outfile.write('[\n')
    for i in json_save_list:
        json.dump(i, outfile)
        outfile.write(',\n')
    outfile.write(']')
with open('data.json', 'r') as file:
    data = file.read().replace('\'','\\"')
    index = data.rfind(",")
    data2 = data[:index] + data[index+1:]
with open("data.json", "w") as outfile:
    outfile.write(data2)
    
print('down...')
