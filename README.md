# 旅游攻略生成器 · Travel Guide Generator

把一句旅行需求变成可编辑的行程手册：每日安排、预算、美食、下雨备选，以及可下载的 HTML、日历和地图点位。

[Claude 安装与使用](references/claude-setup.md) · [三个完整案例](examples/README.md) · [反馈问题](https://github.com/GMMG55/travel-guide-generator/issues)

![实际生成的青岛攻略桌面截图](assets/screenshots/qingdao-desktop.png)

**安装**（运行后选择 Claude Code、Codex 等环境）：

```bash
npx skills add GMMG55/travel-guide-generator
```

全局安装加 `-g`；安装需 Node.js，生成需 Python 3.8+，无需高德 Key。

其他方式：[Prompt 安装](references/claude-setup.md#prompt-安装让-ai-执行安装) · `clawhub install travel-guide-generator` · [Claude 网页端 ZIP / 手动安装](references/claude-setup.md)

安装后试试：

> 帮我生成青岛3天情侣休闲攻略，从北京出发，2人总预算4000元，要有海边、美食和下雨备选。出发日期是〔填写日期〕，不要太赶。

本项目是独立第三方 Agent Skill，采用 Anthropic Skills 所使用的开放技能格式，未被 Anthropic 官方收录或背书。已验证本地构建与安装包结构；Claude Code 和 Claude 网页端的账户内运行尚待实测。静态案例可下载后用浏览器打开，当前不宣称已有在线演示站。

<p align="center">
  <img src="https://img.shields.io/badge/ClawHub-Skill-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/version-2.0.1-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge">
</p>

<p align="center">
  <b>🤖 一句话生成精美旅游攻略 HTML，让每一次出发都有温度</b><br>
  <b>🤖 Generate beautiful travel guide HTML with one sentence. Make every journey warm and memorable.</b>
</p>

---

## ✨ 这是什么？| What is this?

**中文**

旅游攻略生成器是一个 Agent Skill，能够生成详细、可交互的旅游攻略 HTML 页面；安装方式涵盖 Claude 与 ClawHub 渠道。

只需要告诉 AI 你的目的地、出发地、天数和偏好，它就会：

- 🗺️ 规划带时间安排的每日行程，并检查明显的时间冲突
- 🚗 用高德 API 计算景点到景点之间的距离和用时（可选增强，不配也能用）
- 🏨 推荐最合适的住宿区域和酒店
- 🍜 推荐当地地道美食餐厅
- ⚠️ 整理避坑清单（含正确做法 vs 错误做法）
- 💕 加入浪漫时刻提示（情侣向特别优化）
- 📱 生成 **PC + 移动端自适应**的精美 HTML 文件

**English**

Travel Guide Generator is an independent Agent Skill that creates editable travel guides as standalone HTML files. See the Claude setup guide for installation and the current verification scope.

Just tell the AI your destination, departure city, number of days, and preferences. It will:

- 🗺️ Plan daily schedules with conflict checks and clearly marked route estimates
- 🚗 Calculate distances and travel times between spots via Amap API (optional enhancement)
- 🏨 Recommend the best accommodation areas and hotels
- 🍜 Recommend authentic local restaurants
- ⚠️ Compile a pitfall avoidance list (with right vs wrong practices)
- 💕 Add romantic moment tips (optimized for couples)
- 📱 Generate **PC + mobile responsive** beautiful HTML files

---

## 🎯 核心亮点 | Key Features

| 功能 | Feature | 说明 |
|------|---------|------|
| 🗺️ 智能路线规划 | Smart Route Planning | 景点间交通方式+用时自动计算，一目了然 |
| 🏨 酒店住宿推荐 | Hotel Recommendations | 每日行程结束推荐住宿地，注明与次日行程衔接 |
| ⏱️ 可编辑时间表 | Editable Schedule | 点击卡片右上角“编辑”调整时间，路线用时区分估算与实测 |
| ⚠️ 避坑清单 | Pitfall Avoidance | 按目的地提供建议，不固定条数 |
| 🍜 美食推荐 | Food Recommendations | 每餐推荐具体餐厅+人均价格+必点菜 |
| 📱 自适应HTML | Responsive HTML | 同一文件，PC和手机都有完美阅读体验 |
| 🌸 浪漫风格 | Romantic Style | 配色温暖、排版精美，专为情侣休闲设计 |
| 🧭 右侧快速导航 | Quick Navigation | PC端右侧固定导航，弱化设计不喧宾夺主 |
| 📂 可折叠模块 | Collapsible Sections | 点击标题/Day头部可折叠，默认全部展开 |
| 🌍 多语言规划 | Multilingual Planning | 可按需求撰写内容；当前渲染器的固定界面文字以中文为主 |
| 🩺 自动质量检查 | Quality Validation | 检查时间冲突、闭馆日、营业时间、路线衔接和来源时效 |
| 💾 本地交互编辑 | Local Editing | 勾选、收藏、调整时间、顺延后续行程、预算汇总并自动保存 |
| 📤 多格式导出 | Multi-format Export | 同时生成 HTML、Markdown、日历 ICS、GeoJSON 和规范化 JSON |

---

## 🚀 快速开始 | Quick Start

### 安装 | Installation

使用顶部的 `npx` 命令即可；[完整安装指南](references/claude-setup.md)包含指定 Agent、全局安装、Prompt 安装及 ZIP 上传方式。

### 使用 | Usage

首次使用只需三步：安装并启用技能 → 发送旅行需求 → 下载 HTML，用浏览器打开。

Claude Code 可以输入 `/travel-guide-generator` 加需求；Claude 网页端和其他宿主使用自然语言。联网搜索由宿主提供，不能联网时会标注估算与待核实信息。

**中文示例：**
> 帮我生成一份威海4天浪漫攻略，从北京出发，情侣休闲游，不要太紧张

> 生成天津2天周末攻略，高铁去，住一晚，要包含滨海新区

**English Example：**
> Generate a 3-day romantic travel guide for Dalian, departing from Beijing, couple trip

> Create a Shanghai weekend guide for 2 days, include the Bund and Disney

具备联网权限时检索来源，并生成攻略文件。不配置高德 API 也可运行。固定日期、票价和天气都需要出发前重新核实。

### 结构化构建 | Structured Build

v2 使用可校验的数据管线：`guide.json → 路线补全 → 冲突检查 → HTML/Markdown/ICS/GeoJSON`。

```bash
python scripts/build_guide.py examples/sample-guide.json --output-base examples/my-trip
python scripts/validate_guide.py examples/sample-guide.json --strict
```

完整字段格式见 `references/guide-schema.json`。生成后的 HTML 无需服务端，可离线打开；浏览器“打印”可保存为 PDF。

---

## 📸 效果预览 | Preview

查看 [青岛情侣、成都亲子和九寨沟双人案例](examples/README.md)，下载对应 HTML 后即可离线体验；案例不是当前出行建议。

![手机上的行程卡片](assets/screenshots/qingdao-mobile.png)

![点击编辑后显示时间和预算输入框](assets/screenshots/qingdao-edit.png)

生成的攻略 HTML 包含以下模块：

```
🌊 行程亮点（6个核心卖点）
🚄 交通信息（高铁/飞机票价+推荐）
📋 可编辑时间表
📍 Day 1~N 每日行程卡片
   ├── 路线条（含距离和用时）
   ├── 景点详情（含交通提示、游玩时长）
   ├── 浪漫时刻 💕
   ├── 避坑提示 ⚠️
   └── 美食推荐 🍽️
🏨 酒店住宿推荐
⚠️ 按目的地整理的避坑清单
🩺 行程冲突与来源时效检查
🌦️ 天气、季节与室内备选提示
💰 可编辑预算估算
💾 勾选、收藏、时间顺延与本地保存
📤 Markdown / 日历 / GeoJSON 导出
💕 浪漫出行Tips
```

> 💡 **提示：** 可直接打开 `examples/sample-guide-output.html` 查看完整交互示例。

---

## ⚙️ 高级配置（可选增强 · 不配置也能用）| Advanced Configuration (Optional)

> 💡 **先放宽心**：高德 API 是**可选的增强项**，不是必做步骤。即使完全不配置，攻略照常生成——景点间距离和用时会自动用**估算值**代替，行程、酒店、美食、避坑、预算等模块都不受影响。只有你想让路线距离/用时更精准时才需要配置它。

### 高德 API（可选）| Amap API (Optional)

配置高德 Web 服务 API Key 后，可以**自动计算景点到景点之间的真实距离和驾车/步行用时**，路线规划更精准。

**请勿在聊天中把 Key 发送给 AI**（聊天记录可能被留存或泄露）。请自行配置：

```bash
# 临时生效（推荐，仅当前会话有效）
export AMAP_KEY="你的高德API Key"

# 或运行脚本时临时传入：
python scripts/amap_route.py --key "你的高德API Key" --origin "A" --destination "B" --city "城市"
```

> 如需持久化，写入 shell 配置文件（`~/.zshrc` / `~/.bashrc`）或使用系统密钥管理器注入，**不要通过对话让 AI 写入系统环境变量**。一旦 Key 泄露，立即在高德控制台删除并重新生成。

> 申请地址：[高德开放平台](https://lbs.amap.com/)

如果不配置，Skill 会使用近似距离估算，效果也很好 ✅

---

## 🍹 生成的攻略长什么样？| What does the guide look like?

攻略文件是一个**独立的 HTML 文件**，特点：

- 🎨 **渐变色主题**：每天一个配色，视觉层次分明
- 📱 **移动端优化**：768px / 375px 断点自适应
- 💕 **浪漫配色**：粉色/紫色渐变为主色调
- 🖨️ **可打印**：浏览器"打印"即可保存为 PDF

直接双击 HTML 文件在浏览器中打开，或分享给同行伙伴。

---

## 🌍 多语言支持 | Multi-language Support

可请求模型使用以下语言撰写攻略内容。当前渲染器尚未为所有固定按钮、标签实现完整翻译，因此不将其标为已验证的全界面多语言支持。专有名词保留原文，阿拉伯语输出支持设置 RTL 页面方向。

**支持的语言 | Supported Languages**

| 语言代码 | 语言 | 示例请求 |
|----------|------|----------|
| `zh-CN` | 简体中文（默认） | "帮我生成一个威海4天旅游攻略" |
| `en` | 英语 | "Generate a 4-day travel guide for Tokyo" |
| `ja` | 日语 | "東京の4日間旅行ガイドを作成して" |
| `ko` | 韩语 | "부산 4일 여행 가이드 만들어줘" |
| `fr` | 法语 | "Génère un guide de voyage de 4 jours à Paris" |
| `de` | 德语 | "Erstelle einen 4-Tage-Reiseführer für München" |
| `es` | 西班牙语 | "Genera una guía de viaje de 4 días para Barcelona" |
| `it` | 意大利语 | "Genera una guida di viaggio di 4 giorni per Roma" |
| `pt` | 葡萄牙语 | "Gere um guia de viagem de 4 dias para Lisboa" |
| `ru` | 俄语 | "Создай путеводитель на 4 дня по Москве" |
| `th` | 泰语 | "สร้างคู่มือเที่ยวโตเกียว 4 วัน" |
| `vi` | 越南语 | "Tạo hướng dẫn du lịch 4 ngày ở Đà Nẵng" |
| `ar` | 阿拉伯语 | "أنشئ دليلاً سياحياً لمدة 4 أيام في دبي" |

**语言如何自动识别？ | How the language is detected**

- 🗣️ 你用某种语言提问 → 自动用该语言生成攻略
- 🎯 你明确指定语言（如"用英语生成"、"in English"）→ 按指定语言生成
- 🇨🇳 未指定且使用中文 → 默认简体中文

> 💡 阿拉伯语等 RTL（从右到左）语言会自动在 HTML 中添加 `dir="rtl"` 属性，排版自动适配。

---

## 🛠️ 技术架构 | Technical Architecture

```
travel-guide-generator/
├── SKILL.md                          # Skill 主文档
├── assets/
│   └── template.html                 # HTML 模板（含完整CSS）
├── scripts/
│   ├── build_guide.py               # 端到端构建入口
│   ├── validate_guide.py            # 数据校验与冲突检测
│   ├── render_guide.py              # 安全HTML渲染
│   ├── export_guide.py              # Markdown/ICS/GeoJSON导出
│   ├── route_estimator.py           # 无API离线路线估算
│   ├── season_advisor.py            # 天气与季节建议
│   ├── amap_route.py                # 高德API路线规划
│   └── search_guide.py              # 搜索关键词生成
├── references/
│   ├── design-spec.md               # 设计规范
│   ├── daily-itinerary-spec.md      # 每日行程HTML规范
│   └── guide-schema.json            # 结构化攻略Schema
├── examples/                        # JSON与多格式构建示例
├── tests/                           # 离线单元与端到端测试
├── config.json                      # Skill 配置
└── metadata.json                    # Skill 元数据
```

---

## 🤝 贡献 | Contributing

维护者可使用 [案例推广与每周复盘方案](docs/growth-plan.md)，其中包含待发布文案和指标记录模板。

欢迎提交 PR！无论是：
- 🐛 Bug 修复
- ✨ 新功能（如：支持多人行程、增加亲子版本）
- 🌍 增加更多城市模板
- 📖 文档改进

Fork → Branch → PR，我们会尽快审核 🙌

---

## 📝 更新日志 | Changelog

### v2.0.1（2026-09-01）
- 🔒 移除第三方 HTTP 运行时依赖，改用 Python 标准库请求高德 API
- ✅ 保留 Python 3.8+ 兼容性；平台安全扫描结果以发布后实际结果为准

### v2.0.0（2026-09-01）
- 🧱 新增结构化 JSON → 校验 → 渲染 → 多格式导出管线
- 🩺 新增时间冲突、闭馆日、营业时间、交通衔接和来源时效检查
- 🧭 新增高德失败后的经纬度离线路线估算
- 🌦️ 新增天气、南北半球季节建议和高低温提醒
- 💾 新增勾选、收藏、时间顺延、预算汇总及浏览器本地保存
- 📤 新增 Markdown、ICS 日历、GeoJSON 和打印/PDF 支持
- ✅ 新增 Python 3.8/3.12 CI 与端到端测试

### v1.0.8（2026-08-04）
- 🔒 安全加固：移除「把 API Key 粘贴进聊天让 AI 永久写入系统环境变量」的不安全配置指引
- 🔒 改为手动配置 `AMAP_KEY`，并明确警告「勿在聊天中发送密钥」，推荐临时/会话级凭证
- 🔒 在 `metadata.json` / `config.json` 声明网络与环境变量权限，补齐最小权限缺口
- 🎯 收紧自动触发条件：仅明确的攻略生成请求才触发，避免普通旅游闲聊误调外部 API

### v1.0.1（2026-05-19）
- 🧭 新增右侧快速导航（PC端）
- 📂 支持模块折叠（Day卡片、时间表、其他模块）
- 🎨 优化导航颜色和样式
- 🐛 修复Day卡片折叠不生效的问题

### v1.0.0（2026-05-19）
- 🎉 首次发布
- ✅ 景点间交通提示（含距离/用时）
- ✅ 酒店→景点路线条
- ✅ 推荐酒店住宿地模块
- ✅ 精确到分钟的详细时间表
- ✅ 12条避坑清单
- ✅ 游玩用时标注
- ✅ PC/移动端自适应

---

## 📄 许可证 | License

MIT License — 自由使用、修改和分发

---

## 👨‍💻 作者 | Author

由 **GMMG55** 创建，发布到 ClawHub。

- ClawHub: `clawhub install travel-guide-generator`
- GitHub: https://github.com/GMMG55/travel-guide-generator
- Issue 反馈：欢迎在 GitHub Issues 提出

---

<p align="center">
  如果攻略对你有帮助，欢迎在 <a href="https://github.com/GMMG55/travel-guide-generator">GitHub Star 保存项目</a>，或反馈一次真实使用体验。<br>
  If this skill helps you plan a trip, star the repository or share your feedback.
</p>
