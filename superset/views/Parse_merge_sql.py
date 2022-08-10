def json2sql(json_sql):
  sql = json_sql
  col1_sql = ', '.join([f"{sql['Df1']}.{i} AS {sql['Df1']}_{i}" for i in sql['Col1']])
  col2_sql = ', '.join([f"{sql['Df2']}.{i} AS {sql['Df2']}_{i}" for i in sql['Col2']])
  select_sql = "SELECT " + f"{col1_sql}, {col2_sql}"

  from_sql = "FROM " + sql['Df1']

  join_sql = f"{sql['Join']} " + sql['Df2']

  key_sql = [ i['K1'] + " = " + i['K2'] for i in [sql['Key1'], sql['Key2'], sql['Key3'], sql['Key4']] if i['K1'] and i['K2'] != ''] #2022-5-30 + sql['Key3']
  key_sql = key_sql[0] if len(key_sql)==1 else f"( {' AND '.join(key_sql)} )"
  key_sql = "ON " + key_sql


  sql = f"{select_sql} \n{from_sql} \n{join_sql} \n{key_sql}"
  return sql

def Parse_final_res(request_json):
  if type(request_json['sql'])==dict:
    sql = json2sql(request_json['sql'])
    request_json['sql'] = sql

  return request_json
