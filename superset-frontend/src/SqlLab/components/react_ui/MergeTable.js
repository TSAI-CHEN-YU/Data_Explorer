import React from "react";
import {
  Select_col,
  Select_key,
  Select_col2,
  Select_key2,
  Join_opt,
  Add_keys,
  Table_drawer,
  Result_display
} from "./JoinOption"; // opt
import "./MergeTable.css"; //css
import Split from "react-split";
import { Collapse, Button, Layout, Modal } from "antd";
import { backgrounds } from "polished";
const { Header, Footer, Content } = Layout;

// Join type options setting
const styleLink = document.createElement("link");
styleLink.rel = "stylesheet";
styleLink.href = "https://cdn.jsdelivr.net/npm/semantic-ui/dist/semantic.min.css";
// styleLink.href = "./semantic.min.css";
document.head.appendChild(styleLink);

//main function
export default function App() {
  const [visible, setVisible] = React.useState(false); //Merge botton Modal
  return (
    <Layout style={{ overflowY: "scroll", background: "#ececec" }}>
      <Content style={{ margin: "24px 16px 0" }}>
        <div className="leftright">
          <div>
            {/* Button */}
            <Button type="primary" onClick={() => setVisible(true)}>
              Select Data
            </Button>
            <Modal
              title={
                <span className="leftright">
                  <h1>Merge Table</h1> &nbsp;&nbsp;&nbsp;&nbsp;
                  <Table_drawer />
                </span>
              }
              centered
              visible={visible}
              onOk={() => setVisible(false)}
              onCancel={() => setVisible(false)}
              maskClosable={false}
              width={800}
            >
              {/* Data 1 */}
              <div className="leftright">
                <h3 data-toggle="tooltip" title="Select 2 table to merge">
                  Select Data
                </h3>

                <div style={{ height: 10 }} />
              </div>
              <div className="indent">
                <div className="leftright">
                  <Select_col />
                  <div>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <Join_opt />
                  </div>
                  <Select_col2 />
                </div>
                <div style={{ height: 20 }} />
              </div>

              {/* Select Key */}
              <h4 data-toggle="tooltip" title="Select key to merge">
                & Selec key
              </h4>
              <div className="indent">
                <div className="leftright">
                  <Select_key />
                  <h3>&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&nbsp;&nbsp;&nbsp;</h3>
                  <Select_key2 />
                </div>
                <div style={{ height: 20 }} />
                <Add_keys />
                <div style={{ height: 50 }} />
              </div>
            </Modal>
          </div>

          <div style={{ padding: 60 }}>
            <Result_display />
          </div>
        </div>
      </Content>
    </Layout>
  );
}
