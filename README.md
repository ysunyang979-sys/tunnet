# TunNet 实时节点自动同步与聚合订阅

本项目通过 **GitHub Actions** 运行无头后端核心（`tunnet-runtime.exe`），每 1 小时自动同步最新节点，并将其自动转换为 **Clash / Sing-box / V2Ray / Base64** 订阅文件与在线 Web 面板。

---

## 🔗 订阅链接 (永久免费直链)

在客户端添加以下对应的订阅链接即可：

| 客户端类型 | 订阅链接 | 说明 |
| :--- | :--- | :--- |
| **Clash / Mihomo** | `https://ysunyang979-sys.github.io/tunnet/sub/clash.yaml` | 支持 Clash Verge / Clash Meta / Flclash |
| **Sing-box** | `https://ysunyang979-sys.github.io/tunnet/sub/singbox.json` | 支持 Sing-box 1.9+ 订阅 |
| **V2Ray / Shadowrocket** | `https://ysunyang979-sys.github.io/tunnet/sub/vless.txt` | 通用 Base64 订阅源 |
| **纯文本 VLESS 节点** | `https://ysunyang979-sys.github.io/tunnet/sub/nodes.txt` | 单节点连接文本 |

在线订阅面板网址：`https://ysunyang979-sys.github.io/tunnet/`

---

## ⚙️ 开启 GitHub Pages 在线访问

为了让上述订阅链接和在线网页生效，请在 GitHub 仓库中开启 Pages：

1. 打开 GitHub 仓库页面，点击 **Settings**（设置）。
2. 在左侧菜单找到 **Pages**。
3. 在 **Build and deployment** 下方的 **Branch** 中选择 **`main`** 分支，目录选择 **`/ (root)`**。
4. 点击 **Save**（保存）。
5. 等待 1~2 分钟，即可直接通过 `https://ysunyang979-sys.github.io/tunnet/` 在线访问。

---

## ⏱️ 自动化同步机制 (GitHub Actions)

* **执行频率**：每小时整点 (`cron: 0 * * * *`) 自动执行一次。
* **手动触发**：进入仓库的 **Actions** 标签页，点击 **Hourly TunNet Node Sync**，再点击 **Run workflow** 即可随时手动触发立即更新。
