# data2mysql.py [folder] [database] [user] [password]
'''
folder     = convert file's folder path
database   = database name
user       = mysql user name
password   = mysql user password
'''
# ex : python3 data2mysql.py /home/tsaichenyu/獢屸𢒰/data1 NTUHex DataExplorer Stanley1127
# - data must clean
# - defalt mysql host : localhost
import mysql.connector as msql
import pandas as pd
import numpy as np
from mysql.connector import Error
from tqdm import tqdm
from subprocess import call
import glob, os, sys, openpyxl

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

def file_to_csv(f):
    # .txt
    if '.txt' in f:
        with open(f) as text:
            lines = text.readlines(1)[0]
        if ',' in lines:
            df = pd.read_table(f,sep=',')
        else:
            df = pd.read_table(f,sep='\s+')
    # xlsx
    elif '.xlsx' in f:
        df = pd.read_excel(f,engine='openpyxl')
    # csv
    elif '.csv' in f:
        df = pd.read_csv(f)
    # pickle
    elif '.pickle' in f:
        df = pd.read_pickle(f)


    df2 = df.copy()
    #create sample csv (csvsql need)
    df.reset_index(inplace=True)
    df_save = pd.DataFrame(columns=df.columns)
    for col in df.columns:
        # if len(df.loc[df[col].notna(),col]) < 10 and len(df.loc[df[col].notna(),col]) > 0:
        #     i_col = df.loc[df[col].notna(),col].to_list() + [np.nan]*(10-len(df.loc[df[col].notna(),col])) # 2022-7-26
        #     print(f'warnig col: {col} , not enough(10) value')
        # else:
        #     i_col = df.loc[df[col].notna(),col].sample(10).to_list() if np.any(df[col].notna()) else [np.nan]*10
        #     df_save[col] = i_col
        i_col = np.random.choice(df[col].unique(), 10, replace=True) if np.any(df[col].notna()) else [np.nan]*10
        df_save[col] = i_col

    df_save.to_csv("tmp.csv", index=False)
    print('save csv Done.')
    return df2






#-----Auto csv to mysql-----#
##[Create MySQL table] & [Import the CSV data into the MySQL table]
def csv_to_mysql(csv_path, DF, table_name, database_name, dbuser_name, dbuser_passwd, database_port=3306):
    '''
        csv_path   = csv data name
        table_name = data save to mysql's table name
        database   = database name
        user       = mysql user name
        password   = mysql user password
    '''
    
    # # 1. load .csv data
    # df = pd.read_csv(csv_path, index_col=False, low_memory=False)


    # 2. SQL code for create table
    shell_cmd = f'csvsql --dialect mysql --table {table_name} --snifflimit 0 {csv_path} > tmp'
    call(shell_cmd, shell=True)
    
    def read_text(file):
        f = open(file)
        text = f.read()
        f.close
        return text
    sql_create = read_text("tmp")

    sql_create = sql_create.replace('NOT NULL','')

    if 'TIMESTAMP' in sql_create:
        sql_create = sql_create.replace('TIMESTAMP','DATETIME')
    # 2022/7/15
    if type(DF.index) != pd.core.indexes.range.RangeIndex:
        sql_create = sql_create.replace(");",f", INDEX ({','.join(DF.index.names)}) );")

    print('create tmp Done.')

    # 2.5.clean data na (使MySQL可接受)
    # translate none/nan -> null
    DF = DF.astype(object).where(pd.notnull(DF), 'null') ##*** Trans null

    # 2022/7/15
    DF.reset_index(inplace=True)
    print('start conn.')

    # 3. Create a table & Import the CSV data into the MySQL table
    try:
        conn = msql.connect(
            port       = database_port,
            database   = database_name,
            user       = dbuser_name,
            password   = dbuser_passwd,
            host       = "dbDocker",
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
                sql_insert = f"INSERT INTO {database_name}.{table_name} VALUES {tuple(row)}"
                sql_insert = sql_insert.replace("'null'","null") ##*** Trans null
                cursor.execute(sql_insert)
                conn.commit()

            conn.close()
    except Error as e:
        print('MySQL Error:', e)


#-----excute code-----#
Files, Table_name = get_file_path()
for file_path,table_name in zip(Files, Table_name):
    DF = file_to_csv(file_path)
    csv_path      = "tmp.csv"
    database_name = sys.argv[2]
    dbuser_name   = sys.argv[3]
    dbuser_passwd = sys.argv[4]
    

    print(f'Create {table_name} table in {database_name} database...')
    csv_to_mysql(csv_path      = csv_path,
                 DF            = DF,
                 table_name    = table_name,
                 database_name = database_name,
                 dbuser_name   = dbuser_name,
                 dbuser_passwd = dbuser_passwd,
                 database_port = 3306) #db in docker
    
    print(f'Create {table_name} table in {database_name} database Done!')

# shell_cmd = 'rm tmp tmp.csv'
# call(shell_cmd, shell=True)