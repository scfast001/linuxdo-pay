# LINUX DO Credit Payment Demo (Python/Flask)

这是一个基于 Python Flask 框架的 **LINUX DO 积分支付系统** 接入示例。

本项目演示了如何对接 LINUX DO 的 Credit 接口（兼容 EasyPay/易支付协议），并专门针对 **Vercel** Serverless 环境进行了适配，可实现**零成本、高稳定性**的部署。

## ✨ 功能特性

* **发起支付**：自动生成签名 (`sign`) 并构造表单跳转至 LINUX DO 收银台。
* **异步通知 (Notify)**：处理支付结果回调，包含验签逻辑，确保交易安全。
* **同步跳转 (Return)**：处理用户支付完成后的页面回跳。
* **Serverless 适配**：开箱即用，支持一键部署到 Vercel。

## 🛠️ 目录结构

```text
.
├── api
│   └── index.py        # 核心逻辑：包含发起支付、回调处理、签名算法
├── requirements.txt    # 依赖文件 (Flask)
├── vercel.json         # Vercel 路由配置文件
└── README.md           # 说明文档

## 🚀 部署指南 (Vercel)

由于 Vercel 部署需要环境变量，而 LINUX DO 创建应用又需要 Vercel 的域名，建议按以下步骤操作：

### 第一步：准备代码
Fork 本仓库或下载代码并上传到你的 GitHub。

### 第二步：首次部署 (获取域名)
1. 登录 [Vercel](https://vercel.com) 并导入你的 GitHub 项目。
2. 在 **Environment Variables** (环境变量) 设置中，先填入临时数据以完成首次构建：
    * `PID`: `0000`
    * `KEY`: `temp`
3. 点击 **Deploy**。
4. 部署完成后，复制分配给你的域名 (例如: `https://your-project.vercel.app`)。

### 第三步：配置 LINUX DO 应用
1. 前往 [LINUX DO 集市中心](https://credit.linux.do/merchant)。
2. 创建应用，填写如下信息：
    * **应用主页 URL**: `https://your-project.vercel.app`
    * **通知 URL**: `https://your-project.vercel.app/notify`
    * **回调 URL**: `https://your-project.vercel.app/return`
3. 创建成功后，获取真实的 **Client ID (PID)** 和 **Client Secret (Key)**。

### 第三步：更新配置并重新部署
1. 回到 Vercel 项目设置页 (**Settings** -> **Environment Variables**)。
2. 修改 `PID` 和 `KEY` 为你在上一步获取的**真实数据**。
3. 进入 **Deployments** 页面，点击最新一次部署右侧的三个点，选择 **Redeploy**。

## ⚙️ 环境变量说明

| 变量名 | 必填 | 说明 |
| :--- | :--- | :--- |
| `PID` | 是 | 商户 ID (Client ID)，在 LINUX DO 集市中心获取 |
| `KEY` | 是 | 商户密钥 (Client Secret)，**请勿泄露给他人** |

## 🧪 接口说明

* **发起测试**：访问 `/pay`
    * 例如：`https://your-project.vercel.app/pay`
    * 会自动创建一笔测试订单并跳转支付。
* **异步回调**：`/notify`
    * 接收 LINUX DO 发送的 GET 请求，验证签名并返回 `success`。
* **同步回调**：`/return`
    * 用户支付成功后的展示页面。

## 📝 本地开发

如果你想在本地运行：

1. 安装依赖：
   ```bash
   pip install flask

2. 设置环境变量 (Mac/Linux):
export PID="你的PID"
export KEY="你的密钥"

3. 运行：
python api/index.py

## ⚠️ 注意事项
本项目仅作为接入示例，请勿直接用于生产环境。在正式上线前，请务必完善业务逻辑（如数据库写入、防止订单重复处理等）。

请妥善保管你的 KEY，不要将其硬编码在代码文件中。
