import React, { useEffect, useState } from "react";
import "antd/dist/antd.css";
import "./MergeTable.css";
import { Select, Tooltip, message, Button, Drawer } from "antd";
import { Dropdown } from "semantic-ui-react";
import { ProfileOutlined } from "@ant-design/icons";
import data from "./data.json";

// other
const { Option } = Select;
var setKeys,
  setKeyText,
  setKeyvalues,
  setKeys2,
  setKeyText2, //orginal render opt
  setKeyvalues2,
  s_key,
  setKeys_,
  setKeyText_,
  setKeys2_,
  setKeyText2_, //add key opt
  setInfo, //Drawer table info
  setT1_res, //result display
  setC1_res,
  setT2_res,
  setC2_res,
  setTbl_opt_list

// data
// 1.table,column data
var Tables = data.map((i) => i.label); //["A", "B"...];
var Columns = {};
data.map((i) => (Columns[i.label] = i.children.map((j) => j.label))); //{A: ["a", "b", "c"],B: ["a", "b", "c"]

//**refresh real time *2022/7/11
const refreshData=()=>{
  Tables = data.map((i) => i.label); //["A", "B"...];
  Columns = {};
  data.map((i) => (Columns[i.label] = i.children.map((j) => j.label))); //{A: ["a", "b", "c"],B: ["a", "b", "c"]
};

export const RefreshOpt: React.FC = () => {

  useEffect(() => {
    refreshData()
    setTbl_opt_list(Tables)
}, []);
  
  
  const onRefreshOptClick = () => {
    refreshData()
    setTbl_opt_list(Tables)
  };

  return (
    <>
      <Button
        size="small"
        type="dashed"
        onClick={onRefreshOptClick}
        data-toggle="tooltip"
        title="Click to refresh Table drop-down options "
      >
        ⟳
      </Button>
    </>
  );
};


// 2.join opt
const options_join = [
  {
    key: "left",
    value: "LEFT JOIN",
    text: "",
    image: {
      avatar: true,
      src: require("./JoinTypePNG/Left.png")
    }
  },
  {
    key: "right",
    value: "RIGHT JOIN",
    text: "",
    image: {
      avatar: true,
      src: require("./JoinTypePNG/Right.png")
    }
  },
  {
    key: "inner",
    value: "INNER JOIN",
    text: "",
    image: {
      avatar: true,
      src: require("./JoinTypePNG/Inner.png")
    }
  }
];

// main
// 1(1).select cloumns (want to merge)
export const Select_col = () => {
  //refresh
  const [tbl_opt_list, setTbl_opt_list] = useState([]);
  useEffect(() => {
    refreshData()
    setTbl_opt_list(Tables)
    // console.log(Tables.length)
  }, []);

  const [tables, setTables] = useState([]);
  const [columns, setColumns] = useState([]);

  const tableChange = (value) => {
    setTables(Columns[value]); //set columns
    setColumns([]); //reset column value
    // set first key
    setKeys(Columns[value]); //set keys
    setKeyText(value); //table text in key opt
    setKeyvalues(null); //key value refresh
    // set add key
    s_key([]); //reset add key
    setKeys_(Columns[value]); //set keys
    setKeyText_(value); //table text in key opt
    // display result
    setT1_res(value);
    //set final result
    final_res.Df1 = value;
  };

  const columnChange = (value) => {
    setColumns(value); //catch column value
    // display result
    setC1_res(value);
    //set final result
    final_res.Col1 = value;
  };

  return (
    <>
      <Select
        showSearch
        placeholder="Data 1..."
        style={{ width: 150 }}
        onChange={tableChange}
      >
        {tbl_opt_list.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>
      <Select
        mode="multiple"
        allowClear
        maxTagCount={0}
        style={{ width: 150 }}
        placeholder="Columns..."
        value={columns}
        onChange={columnChange}
      >
        {tables.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>
    </>
  );
};
// 2(1).select key
export const Select_key = () => {
  // opt
  const [key, setKey] = useState([]);
  const [keyvalue, setKeyvalue] = useState([]);
  setKeys = setKey;
  setKeyvalues = setKeyvalue; //2022-2-10
  // text
  const [text, setText] = useState("Data1");
  setKeyText = setText;

  const setKeyvalueChange = (value) => {
    setKeyvalue(value); //catch column value
    //set final result
    final_res.Key1.K1 = `${text}.${value}`;
  };

  return (
    <span>
      <p className="key_equal">{text}</p>
      <Select
        style={{ width: 150 }}
        placeholder="Columns..."
        value={keyvalue}
        onChange={setKeyvalueChange}
        size={"small"}
      >
        {key.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>
    </span>
  );
};
// 1(2).select cloumns (want to merge)
export const Select_col2 = () => {

  const [tables, setTables] = useState([]);
  const [columns, setColumns] = useState([]);

  const tableChange = (value) => {
    setTables(Columns[value]); //set columns
    setColumns([]); //reset column value
    // set first key
    setKeys2(Columns[value]); //set keys
    setKeyText2(value); //table text in key opt
    setKeyvalues2(null); //key value refresh
    // set add key
    s_key([]); //reset add key
    setKeys2_(Columns[value]); //set keys
    setKeyText2_(value); //table text in key opt
    // display result
    setT2_res(value);
    //set final result
    final_res.Df2 = value;
  };

  const columnChange = (value) => {
    setColumns(value); //catch column value
    // display result
    setC2_res(value);
    //set final result
    final_res.Col2 = value;
  };

  return (
    <>
      <Select
        showSearch
        placeholder="Data 2..."
        style={{ width: 150 }}
        onChange={tableChange}
      >
        {Tables.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>
      <Select
        mode="multiple"
        allowClear
        maxTagCount={0}
        style={{ width: 150 }}
        placeholder="Columns..."
        value={columns}
        onChange={columnChange}
      >
        {tables.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>
    </>
  );
};
// 2(2).select key
export const Select_key2 = () => {
  // opt
  const [key, setKey] = useState([]);
  const [keyvalue, setKeyvalue] = useState([]);
  setKeys2 = setKey;
  setKeyvalues2 = setKeyvalue; //2022-2-10
  // text
  const [text, setText] = useState("Data2");
  setKeyText2 = setText;

  const setKeyvalueChange = (value) => {
    setKeyvalue(value); //catch column value
    //set final result
    final_res.Key1.K2 = `${text}.${value}`;
  };

  return (
    <span>
      <p className="key_equal">{text}</p>
      <Select
        style={{ width: 150 }}
        placeholder="Select columns..."
        value={keyvalue}
        onChange={setKeyvalueChange}
        size={"small"}
      >
        {key.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>
    </span>
  );
};
// 3.Join selection
export const Join_opt = () => {
  const [option3, setOption3] = useState("LEFT JOIN"); //tooltip display select
  const onChange = (event, data) => {
    var tooltip_key = data.value;
    setOption3(tooltip_key);
    //set final result
    final_res.Join = tooltip_key;
  };
  return (
    <span>
      <Tooltip title={option3}>
        <Dropdown
          inline
          options={options_join}
          defaultValue={options_join[0].value}
          onChange={onChange}
        />
      </Tooltip>
    </span>
  );
};
// 4.Add more key
export const Add_keys = () => {
  //---key1
  const [key, setKey] = useState([]);
  setKeys_ = setKey;

  // text1
  const [text, setText] = useState("Data1");
  setKeyText_ = setText;

  //---key2
  const [key2, setKey2] = useState([]);
  setKeys2_ = setKey2;

  // text2
  const [text2, setText2] = useState("Data2");
  setKeyText2_ = setText2;

  //---add keys
  const [AddkeyList, setAddkeyList] = useState([]);
  s_key = setAddkeyList;

  const setAddkey1Change = (value) => {
    if (AddkeyList.length === 0) final_res.Key2.K1 = `${text}.${value}`;
    if (AddkeyList.length === 1) final_res.Key3.K1 = `${text}.${value}`;
    if (AddkeyList.length === 2) final_res.Key4.K1 = `${text}.${value}`;
  }; // add key1 result
  const setAddkey2Change = (value) => {
    if (AddkeyList.length === 0) final_res.Key2.K2 = `${text2}.${value}`;
    if (AddkeyList.length === 1) final_res.Key3.K2 = `${text2}.${value}`;
    if (AddkeyList.length === 2) final_res.Key4.K2 = `${text2}.${value}`;
    // console.log(final_res);
  }; // add key2 result

  const onAddBtnClick = () => {
    if (AddkeyList.length < 3) {
      s_key(
        AddkeyList.concat(
          <span key={AddkeyList.length}>
            <div style={{ height: 50 }} className="leftright">
              <span>
                <p className="key_equal">{text}</p>
                <Select
                  style={{ width: 150 }}
                  size={"small"}
                  placeholder="Columns..."
                  onChange={setAddkey1Change}
                >
                  {key.map((table) => (
                    <Option value={table} key={table}>
                      {table}
                    </Option>
                  ))}
                </Select>
              </span>

              <h3>&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&nbsp;&nbsp;&nbsp;</h3>

              <span>
                <p className="key_equal">{text2}</p>
                <Select
                  style={{ width: 150 }}
                  size={"small"}
                  placeholder="Select columns..."
                  onChange={setAddkey2Change}
                >
                  {key2.map((table) => (
                    <Option value={table} key={table}>
                      {table}
                    </Option>
                  ))}
                </Select>
              </span>
            </div>
          </span>
        )
      );
    } else {
      message.warning("Maximum 4 keys");
      // setInputList(state:)
    }
  };
  return (
    <span>
      <Button
        size="small"
        type="dashed"
        onClick={onAddBtnClick}
        data-toggle="tooltip"
        title="Click to add more key "
      >
        +
      </Button>
      <div style={{ height: 5 }} />
      {AddkeyList}
    </span>
  );
};
// 5.Drawer (table introduction)
const Table_info = () => {
  const [tables, setTables] = useState([]);
  const [columns, setColumns] = useState([]);

  const tableChange = (value) => {
    setTables(Columns[value]); //set columns
    setColumns([]); //reset column value
    // set first key
    setKeys(Columns[value]); //set keys
    setKeyText(value); //table text in key opt
    // set add key
    s_key([]); //reset add key
    setKeys_(Columns[value]); //set keys
    setKeyText_(value); //table text in key opt
  };

  const columnChange = (value) => {
    setColumns(value); //catch column value
    let res = data
      .map((i) => i.children.filter((j) => j.label === value))
      .filter((item) => item.length > 0)[0][0].description;
    return setInfo(res);
  };
  //display info
  const [info, setInformation] = useState("Select Table to view description");
  setInfo = setInformation;
  return (
    <div>
      <Select
        showSearch
        placeholder="Data 1..."
        style={{ width: 200 }}
        onChange={tableChange}
      >
        {Tables.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>
      <Select
        style={{ width: 200 }}
        placeholder="Columns..."
        value={columns}
        onChange={columnChange}
      >
        {tables.map((table) => (
          <Option value={table} key={table}>
            {table}
          </Option>
        ))}
      </Select>

      <div style={{ height: 20 }} />
      <p>{info}</p>
    </div>
  );
};
export const Table_drawer = () => {
  const [visible, setVisible] = useState(false);

  const showDrawer = () => {
    setVisible(true);
  };

  const onClose = () => {
    setVisible(false);
  };

  return (
    <>
      <ProfileOutlined
        onClick={showDrawer}
        data-toggle="tooltip"
        title="click to see table description "
      />
      <a
        href="#"
        onClick={showDrawer}
        data-toggle="tooltip"
        title="click to see table description "
      >
        &nbsp;table description
      </a>
      <Drawer
        title="Table description"
        placement="right"
        onClose={onClose}
        visible={visible}
        width={450}
      >
        <p>Search table</p>
        <Table_info />
      </Drawer>
    </>
  );
};
// 6.Display result
export const Result_display = () => {
  const [t1_res, setT1_result] = useState([]);
  const [c1_res, setC1_result] = useState([]);
  const [t2_res, setT2_result] = useState([]);
  const [c2_res, setC2_result] = useState([]);
  setT1_res = setT1_result;
  setC1_res = setC1_result;
  setT2_res = setT2_result;
  setC2_res = setC2_result;
  // className="textindent"
  return (
    <div>
      <div style={{ height: 50 }} />
      {/* <p>select table:</p> */}
      {t1_res}
      <div style={{ display: "flex" }}>
        <li style={{ padding: 15 }} />
        {c1_res.map((list) => (
          <li style={{ padding: 5 }}>{`"${list}",`}</li>
        ))}
      </div>
      {t2_res}
      <div style={{ display: "flex" }}>
        <li style={{ padding: 15 }} />
        {c2_res.map((list) => (
          <li style={{ padding: 5 }}>{`"${list}",`}</li>
        ))}
      </div>
    </div>
  );
};

// 7.User's final result
export const final_res = {
  Df1: "",
  Col1: "",
  Df2: "",
  Col2: "",
  Join: "LEFT JOIN",
  Key1: { K1: "", K2: "" },
  Key2: { K1: "", K2: "" },
  Key3: { K1: "", K2: "" },
  Key4: { K1: "", K2: "" }
};
