pip install mysqlclient>=2.1.0 tqdm>=4.64.0 mysql-connector>=2.2.9 pandas>=1.3.4 subprocess.run>=0.0.8 openpyxl>=3.0.7 csvkit>=1.0.7

echo "222222222222222222222222222222222222"
py_path="/app/input_your_file"
file_path="/app/input_your_file/your_files"

echo "Starting load data..."
python "${py_path}"/data2mysql.py "${file_path}" NTUHex DataExplorer Stanley1127
cd "${py_path}"

echo "Starting modify merge ui option..."
python colnames2json.py "${file_path}"
cp "${py_path}"/data.json /app/superset-frontend/src/SqlLab/components/react_ui
