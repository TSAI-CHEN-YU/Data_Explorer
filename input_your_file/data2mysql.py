# Copyright 2022 國立臺灣大學人工智慧中心

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# data2mysql.py [data folder path] [db name] [db user] [db password] [db host] [db port]
'''
folder     = convert file's folder path
database   = database name
user       = mysql user name
password   = mysql user password
'''
# ex : python3 data2mysql.py /home/tsaichenyu/獢屸𢒰/data1 NTUHex DataExplorer Stanley1127 dbDocker 3306
# - data must clean
# - defalt mysql host : localhost
import mysql.connector as msql
import pandas as pd
import numpy as np
from mysql.connector import Error
from tqdm import tqdm
from subprocess import call
import glob, os, json, sys, openpyxl, re

def xlsx_sheet_split(Files): #2022/7/18 *xlsx sheet split
    for f in Files:
        if ".xlsx" in f: 
            # 若包含多個sheet，切割為多個xlsx檔，命名為"{表單名稱}_{sheet名稱}"，存在 /tmp底下
            wb = openpyxl.load_workbook(f)
            if len(wb.sheetnames)!=1:
                Files.remove(f)

                # add split file to /tmp
                for i in wb.sheetnames:
                    save_name = f"{os.path.basename(os.path.splitext(f)[0])}_{i}.xlsx"
                    s_path = f"{os.path.dirname(f)}/tmp"
                    if f'{i}.xlsx' not in pd.Series(glob.glob(s_path+'/*')).apply(lambda i : os.path.basename(i)).to_list():
                        df2 = pd.read_excel(f, sheet_name = i, engine='openpyxl')
                        # s_path = f"{os.path.dirname(f)}/tmp/{os.path.basename(os.path.splitext(f)[0])}_{i}.pickle"
                        # df2.to_pickle(s_path)
                        df2.to_excel(f'{s_path}/{save_name}', index=False)

                    # add path
                    Files.append(f'{s_path}/{save_name}')            
    return Files 

def get_file_path():
    path = sys.argv[1] if len(sys.argv) > 1 else []
    files = glob.glob(os.path.join(path, "*.csv"))+glob.glob(os.path.join(path, "*.xlsx"))+glob.glob(os.path.join(path, "*.txt"))+glob.glob(os.path.join(path, "*.pickle"))

    # xlsx sheet split
    files = xlsx_sheet_split(files)

    files_name = [os.path.basename(i) for i in files]
    table_name = [i.split('.')[0] for i in files_name]

    print('files:',files_name)
    return files, table_name

def data_to_csv(f):
    # .txt
    if '.txt' in f:
        try:
            with open(f,'r',encoding='utf-8') as text:
                lines = text.readlines(1)[0]
        except UnicodeDecodeError:
            with open(f,'r',encoding='cp950', errors="ignore") as text:
                lines = text.readlines(1)[0]
        if ',' in lines:
            try:
                df = pd.read_csv(f,sep=',',encoding='utf-8',low_memory=False)
            except UnicodeDecodeError:
                df = pd.read_csv(f,sep=',',encoding='cp950',encoding_errors='ignore',low_memory=False)
        else:
            try:
                df = pd.read_csv(f,sep='\t',encoding='utf-8',low_memory=False)
            except UnicodeDecodeError:
                df = pd.read_csv(f,sep='\t',encoding='cp950',encoding_errors='ignore',low_memory=False)
    # xlsx
    elif '.xlsx' in f:
        df = pd.read_excel(f,engine='openpyxl')
    # csv
    elif '.csv' in f:
        try:
            df = pd.read_csv(f,encoding='utf-8',low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(f,encoding='big5',encoding_errors='ignore',low_memory=False)
    # pickle
    elif '.pickle' in f:
        df = pd.read_pickle(f)


    df2 = df.copy()
    #create sample csv (csvsql need)
    df.reset_index(inplace=True)
    df_save = pd.DataFrame(columns=df.columns)
    np.random.seed(0)
    for col in df.columns:
        i_col = np.random.choice(df[col].unique(), 100, replace=True) if np.any(df[col].notna()) else [np.nan]*100
        df_save[col] = i_col

    df_save.to_csv("tmp.csv", index=False)
    print('save csv Done.')
    return df2

#-----Create DB json file(columns2json.py)-----#
def create_json(df, table_name):
    # file columns
    colnames = list(df.columns)
    #tablecol = [f'{table_name}.{i}' for i in colnames]

    # json element
    json_save = dict(label=table_name,
                    title=table_name,
                    value=table_name,
                    children=[dict(label=i,
                                    title=i,
                                    value=f'{table_name}.{i}',
                                    description='some description...') for i in colnames]
                    )
    return json_save

#-----modify csvkit-csvsql result-----#
def replace_Misjudgment(sql_create,df_tmp,table_name):
    # csvsql判斷格式錯誤，需要修改，包括：1.全部空值；2.時間格式為HHMMSS；3.0開頭的數值(ex:0011)；*4.全部相同值(1,0,N,Y)
    replace_Misjudgment_list = []
    # 1.全部空值-12
    l1 = [
        ['C548_03_DEATHNOTIFY'           ,'OTHERPLACE'            ,'BOOL','VARCHAR(10)'],
        ['C548_19_SYBASE_noBA'           ,'ISHEALTHEXAM'          ,'BOOL','VARCHAR(10)'],
    ]
    # 2.時間格式為HHMMSS-8
    l2 = [
        ['C548_19_SYBASE_noBA'  ,'LOGTIME'                       ,'DECIMAL','TIME'],
        ['C548_20_SYBASE_BA'    ,'LOGTIME'                       ,'DECIMAL','TIME'],
    ]
    # 3.零開頭的數值(ex:0011)-45
    l3 = [
        ['C548_01_PATIENTDEMOGRAPHICS'      ,'NATIONALCODE'         ,'DECIMAL','VARCHAR(20)'],
        ['C548_01_PATIENTDEMOGRAPHICS'      ,'REGISTERZIPAREACODE'  ,'DECIMAL','VARCHAR(20)'],
    ]
    # 4.全部相同值(1,0,N,Y)-29
    l4 = []
    error_list = ['N','Y','0','1','T']
    for col in df_tmp.columns:
        org_str = re.findall(f'`?{col}`? (.*?)\n', sql_create)[0] 
        # 若csvsql判斷(1,0,N,Y)為 Boolean，做修正
        if 'BOOL' in org_str: 
            df_valuecounts_name = df_tmp[col].value_counts().index
            if len(df_valuecounts_name) == 1 and str(df_valuecounts_name[0]) in error_list:
                for err in error_list :
                    lg = str(df_valuecounts_name[0])==err
                    if lg:
                        currect = 'VARCHAR(10)' if err in ['N','Y','T'] else 'DECIMAL(1, 0)' #1,0
                        l4.append([table_name,col,'BOOL',currect])

    replace_Misjudgment_list = l1+l2+l3+l4
    for L in list(filter(lambda i: i[0] == table_name, replace_Misjudgment_list)):
        print('\t→'.join(L))
    # print('\n'.join(['\t→'.join(i) for i in replace_Misjudgment_list]))
    # start replace
    for i in replace_Misjudgment_list:
        if i[0] in sql_create:
            # if () in type
            if i[2] in ['VARCHAR','DECIMAL']:
                org_str = f'`{i[1]}` ' + re.findall(f'`{i[1]}` (.*?)\n', sql_create)[0]
                rep_str = f"`{i[1]}` {i[3]}, " if ',' in org_str[-2:] else f"`{i[1]}` {i[3]}"
            else:
                org_str = f"`{i[1]}` {i[2]}"
                rep_str = f"`{i[1]}` {i[3]}"
            # print(org_str,'---',rep_str)
            sql_create = sql_create.replace(org_str,rep_str)

    return sql_create



#-----Auto data to mysql-----# 
##取得小樣本csv檔 > 讀取小樣本csv檔，建構sql表 > 將資料一行行插入sql表
##[Create MySQL table] & [Import the data into the MySQL table]
def data_to_mysql(csv_path, DF, table_name, database_name, dbuser_name, dbuser_passwd, database_host, database_port):
    '''
        csv_path      = sample data(csv) path
        DF            = data's DataFrame
        table_name    = data save to db's table name
        database_name = db name
        dbuser_name   = db user name
        dbuser_passwd = db user password
        database_host = db host
        database_port = db port
    '''
    
    # # 1. load .csv data
    # df = pd.read_csv(csv_path, index_col=False, low_memory=False)


    # 2. SQL code for create table *pip install csvkit
    shell_cmd = f'csvsql --dialect mysql --table {table_name} --snifflimit 0 {csv_path} > tmp'
    call(shell_cmd, shell=True)
    
    def read_text(file):
        f = open(file)
        text = f.read()
        f.close
        return text

    sql_create = read_text("tmp")
    df_tmp = pd.read_csv("tmp.csv")
    sql_create = replace_Misjudgment(sql_create,df_tmp,table_name)
    sql_create = sql_create.replace(' NOT NULL','').replace(' NULL','').replace('TIMESTAMP','DATETIME')
    # 2022/7/15
    if type(DF.index) != pd.core.indexes.range.RangeIndex:
        sql_create = sql_create.replace(");",f", INDEX ({','.join(DF.index.names)}) );")

    print('create tmp(SQL Create table) Done.')

    # 2.5.clean data na (使MySQL可接受)
    # translate none/nan -> null
    DF = DF.astype(object).where(pd.notnull(DF), 'null') ##*** Trans null

    # 2022/7/15
    DF.reset_index(inplace=True)
    print('start conn.')

    # convert bool
    for i in DF.columns:
        if set(DF[i].unique()) == set(['N', 'Y']):
            DF[i] = DF[i] == 'Y'

    # 3. Create a table & Import the CSV data into the MySQL table
    try:
        conn = msql.connect(
            database   = database_name,
            user       = dbuser_name,
            password   = dbuser_passwd,
            host       = database_host,
            port       = database_port,
            auth_plugin= "mysql_native_password",
        )
        if conn.is_connected():
            cursor = conn.cursor()
            #mysql set
            cursor.execute("SET @@global.sql_mode= '';")
            #csv to mysql
            print(sql_create)
            cursor.execute(sql_create)
            print('create done.')
            for i, row in tqdm(DF.iterrows(), total=DF.shape[0]):
            # for i, row in DF.iterrows():
                sql_insert = f"INSERT INTO {database_name}.{table_name} VALUES {tuple(row)}"
                sql_insert = sql_insert.replace("'null'","null") ##*** Trans null
                cursor.execute(sql_insert)
                conn.commit()

            conn.close()
    except Error as e:
        print('MySQL Error:', e)


#-----excute code-----#
Files, Table_name = get_file_path()
json_save_list = []
for file_path,table_name in sorted(zip(Files, Table_name), key=lambda x: x[1]):
    DF = data_to_csv(file_path)
    csv_path      = "tmp.csv"
    database_name = sys.argv[2]
    dbuser_name   = sys.argv[3]
    dbuser_passwd = sys.argv[4]
    database_host = sys.argv[5]
    database_port = sys.argv[6]
    ## create json file
    json_save = create_json(DF, table_name)
    json_save_list.append(json_save)
    ## data to sql table
    print(f'Create {table_name} table in {database_name} database...')
    data_to_mysql(csv_path      = csv_path,    #小樣本csv檔
                DF            = DF,            #原始資料
                table_name    = table_name,    #sql的table名稱
                database_name = database_name, #sql的shema名稱
                dbuser_name   = dbuser_name,   #sql的user
                dbuser_passwd = dbuser_passwd, #sql的password
                database_host = database_host, #host
                database_port = database_port) #sql使用的port
    
    print(f'Create {table_name} table in {database_name} database Done!')

# output .json file(data_table.json)
directory = os.path.dirname(sys.argv[0])
with open(f"{directory}/data.json", "w") as outfile:
    outfile.write('[\n')
    for i in json_save_list:
        json.dump(i, outfile)
        outfile.write(',\n')
    outfile.write(']')
with open(f"{directory}/data.json", "r") as file:
    data = file.read().replace('\'','\\"')
    index = data.rfind(",")
    data2 = data[:index] + data[index+1:]
with open(f"{directory}/data.json", "w") as outfile:
    outfile.write(data2)
