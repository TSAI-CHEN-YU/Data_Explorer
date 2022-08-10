import React, { useState } from "react";
import { Steps, Card, Row, Button } from "antd";
import { useScrollTo } from "react-use-window-scroll";
import HomePNG from "./Home.png";

const { Step } = Steps;
//<a href="#top">Back to top</a>
const HookExample = () => {
  const scrollTo = useScrollTo();
  return (
    <div>
      <Button
        size={"large"}
        style={{ background: "FFCC00", borderColor: "yellow" }}
        onClick={() => scrollTo({ top: 0, left: 0, behavior: "smooth" })}
      >
        <mark>Start from the top menu</mark>
      </Button>
    </div>
  );
};
const tabListNoTitle = [
  {
    key: "Dashboards",
    tab: "Dashboards"
  },
  {
    key: "Merge",
    tab: "Preview & Merge Data"
  },
  {
    key: "Datasets",
    tab: "Datasets"
  }
];
const contentListNoTitle = {
  Dashboards: (
    <ul
      style={{
        fontFamily: "Georgia",
        fontSize: 15
      }}
    >
      <p>
        Refer to the visual analysis example and change the table used for
        analysis
      </p>
      <br />
    </ul>
  ),
  Merge: (
    <ul
      style={{
        fontFamily: "Georgia",
        fontSize: 15
      }}
    >
      <p>Merge multiple tables for analysis</p>
      <br />
      <br />
      <br />
    </ul>
  ),
  Datasets: (
    <ul
      style={{
        fontFamily: "Georgia",
        fontSize: 15
      }}
    >
      <p>Select a table for analysis</p>
      <br />
      <br />
      <br />
    </ul>
  )
};

export const Home_content = () => {
  const [activeTabKey, setActiveTabKey] = useState("Dashboards");

  const onTabChange = (key: React.SetStateAction<string>) => {
    setActiveTabKey(key);
  };

  return (
    <div>
      <br />
      <h1
        style={{
          textAlign: "center",
          fontFamily: "Comic Sans MS",
          fontSize: 48
        }}
      >
        Welcome to Data Explorer !
      </h1>
      <br />
      <br />
      <br />
      <br />
      <h3
        style={{
          textAlign: "center",
          fontFamily: "Georgia",
          fontSize: 40,
          fontWeight: "bold"
        }}
      >
        <u>Steps</u>
      </h3>
      <Row justify="center">
        <img src={require("./HomeImage/Home.png")} alt="step" height="600" />
      </Row>
      <br />
      <br />
      <br />
      <br />
      <br />
      <h3
        style={{
          textAlign: "center",
          fontFamily: "Georgia",
          fontSize: 40,
          fontWeight: "bold"
          // marginLeft: "350px"
        }}
        data-toggle="tooltip"
        title="Introduction of 3 methods"
      >
        <u>Explore methods</u>
      </h3>

      <br />

      <Row justify="center">
        <Card
          style={{
            width: 465,
            fontFamily: "Comic Sans MS",
            backgroundColor: "transparent"
          }}
          bordered={false}
          tabList={tabListNoTitle}
          activeTabKey={activeTabKey}
          onTabChange={(key) => {
            onTabChange(key);
          }}
        >
          {contentListNoTitle[activeTabKey]}
        </Card>
      </Row>
      <br />
      <p
        style={{
          textAlign: "center",
          fontFamily: "Comic Sans MS",
          fontSize: 18
        }}
      >
        <HookExample />
        <br />
      </p>
    </div>
  );
};
