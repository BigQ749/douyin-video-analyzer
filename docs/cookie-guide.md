# 获取抖音 cookies 指南

本工具需要抖音登录 cookies 才能获取视频源地址。推荐以下两种方式之一。

## 方式一：使用 douyin-downloader 的 cookie_fetcher（推荐）

### 安装 douyin-downloader

```bash
git clone https://github.com/jiji262/douyin-downloader.git
cd douyin-downloader
pip install -r requirements.txt
cp config.example.yml config.yml
```

### 扫码获取 cookies

```bash
python -m tools.cookie_fetcher --config config.yml
```

1. 会自动打开一个浏览器窗口
2. 在浏览器中扫码登录你的抖音账号
3. 登录成功后，回到终端按 `Enter`
4. cookies 会自动写入 `config.yml`

### 复制 cookies 到本工具

将 `config.yml` 中的 `cookies:` 部分复制到本工具的配置文件中。

## 方式二：手动从浏览器导出

1. 在 Chrome/Edge 中打开 `https://www.douyin.com/` 并登录
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` → `Cookies` → `www.douyin.com`
4. 找到以下关键字段并复制值：

| 字段 | 说明 | 有效期 |
|------|------|--------|
| `sessionid` | 登录会话 ID | 约 60 天 |
| `ttwid` | 设备标识 | 长期 |
| `msToken` | 反爬 Token | 短期，需定期更新 |

5. 创建 `config.yml`：

```yaml
cookies:
  sessionid: "你的sessionid"
  ttwid: "你的ttwid"
  msToken: "你的msToken"
```

## 注意事项

- `sessionid` 有效期约 60 天，过期后需重新获取
- `msToken` 有效期较短，建议每次使用前刷新
- 不要将 `config.yml` 提交到 Git 仓库（已在 `.gitignore` 中排除）
- 如果视频解析失败，通常是 `msToken` 过期，重新获取即可
