const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

// 解析 JSON 請求
app.use(express.json());

// 提供靜態文件
app.use(express.static("public"));

// 定義一個 POST 路由來接收數據
app.post("/submit", (req, res) => {
  const userData = req.body;
  console.log(userData); // 輸出接收到的數據
  res.status(200).send("數據已接收");
});

// 啟動伺服器
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
