# 🌍 旅游攻略生成器 · Travel Guide Generator

<p align="center">
  <img src="https://img.shields.io/badge/QClaw-Skill-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge">
</p>

<p align="center">
  <b>🤖 一句话生成精美旅游攻略 HTML，让每一次出发都有温度</b><br>
  <b>🤖 Generate beautiful travel guide HTML with one sentence. Make every journey warm and memorable.</b>
</p>

---

## ✨ 这是什么？| What is this?

**中文**

旅游攻略生成器是一个 QClaw Skill，能够**自动生成精美、详细、可交互的旅游攻略 HTML 页面**。

只需要告诉 AI 你的目的地、出发地、天数和偏好，它就会：

- 🗺️ 自动规划每日详细行程（精确到分钟）
- 🚗 用高德 API 计算景点到景点之间的距离和用时
- 🏨 推荐最合适的住宿区域和酒店
- 🍜 推荐当地地道美食餐厅
- ⚠️ 整理避坑清单（含正确做法 vs 错误做法）
- 💕 加入浪漫时刻提示（情侣向特别优化）
- 📱 生成 **PC + 移动端自适应**的精美 HTML 文件

**English**

Travel Guide Generator is a QClaw Skill that **automatically generates beautiful, detailed, and interactive travel guide HTML pages**.

Just tell the AI your destination, departure city, number of days, and preferences. It will:

- 🗺️ Auto-plan daily itinerary (accurate to the minute)
- 🚗 Calculate distances and travel times between spots via Amap API
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
| ⏱️ 精确到分钟 | Minute-Accurate Schedule | 不再模糊的"上午/下午"，精确到几点几分 |
| ⚠️ 12条避坑清单 | Pitfall Avoidance | 用删除线标出错误做法，绿色标出正确做法 |
| 🍜 美食推荐 | Food Recommendations | 每餐推荐具体餐厅+人均价格+必点菜 |
| 📱 自适应HTML | Responsive HTML | 同一文件，PC和手机都有完美阅读体验 |
| 🌸 浪漫风格 | Romantic Style | 配色温暖、排版精美，专为情侣休闲设计 |

---

## 🚀 快速开始 | Quick Start

### 安装 | Installation

```bash
# 方式一：通过 ClawHub 安装（推荐）
clawhub install travel-guide-generator

# 方式二：通过 OpenClaw 安装
openclaw skills install travel-guide-generator
```

### 使用 | Usage

安装后，直接在 OpenClaw 对话中说出你的需求：

**中文示例：**
> 帮我生成一份威海4天浪漫攻略，从北京出发，情侣休闲游，不要太紧张

> 生成天津2天周末攻略，高铁去，住一晚，要包含滨海新区

**English Example：**
> Generate a 3-day romantic travel guide for Dalian, departing from Beijing, couple trip

> Create a Shanghai weekend guide for 2 days, include the Bund and Disney

AI 会自动搜索真实攻略信息，生成精美的 HTML 文件并提供下载。

---

## 📸 效果预览 | Preview

生成的攻略 HTML 包含以下模块：

```
🌊 行程亮点（6个核心卖点）
🚄 交通信息（高铁/飞机票价+推荐）
📋 详细时间表（精确到分钟）
📍 Day 1~N 每日行程卡片
   ├── 路线条（含距离和用时）
   ├── 景点详情（含交通提示、游玩时长）
   ├── 浪漫时刻 💕
   ├── 避坑提示 ⚠️
   └── 美食推荐 🍽️
🏨 酒店住宿推荐
⚠️ 避坑清单（12条）
💰 预算估算
💕 浪漫出行Tips
```

> 💡 **提示：** 效果图请查看本仓库的 `examples/` 目录（待补充）

---

## ⚙️ 高级配置 | Advanced Configuration

### 高德 API（可选）| Amap API (Optional)

配置高德 Web 服务 API Key 后，可以**自动计算景点到景点之间的真实距离和驾车/步行用时**，路线规划更精准：

```bash
# 设置环境变量
export AMAP_KEY="你的高德API Key"

# 或者在 OpenClaw 中告知 AI：
# "我的高德API Key是 xxx，生成攻略时帮我计算真实距离"
```

> 申请地址：<ADDRESS_REDACTED>

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

## 🛠️ 技术架构 | Technical Architecture

```
travel-guide-generator/
├── SKILL.md                          # Skill 主文档
├── assets/
│   └── template.html                 # HTML 模板（含完整CSS）
├── scripts/
│   ├── amap_route.py                # 高德API路线规划
│   └── search_guide.py             # 搜索攻略内容
├── references/
│   ├── design-spec.md               # 设计规范
│   └── daily-itinerary-spec.md     # 每日行程HTML规范
├── config.json                      # Skill 配置
└── metadata.json                    # Skill 元数据
```

---

## 🤝 贡献 | Contributing

欢迎提交 PR！无论是：
- 🐛 Bug 修复
- ✨ 新功能（如：支持多人行程、增加亲子版本）
- 🌍 增加更多城市模板
- 📖 文档改进

Fork → Branch → PR，我们会尽快审核 🙌

---

## 📝 更新日志 | Changelog

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

由 **QClaw 用户** 创建，发布到 ClawHub。

- ClawHub: `clawhub install travel-guide-generator`
- GitHub: https://github.com/GMMG55/travel-guide-generator
- Issue 反馈：欢迎在 GitHub Issues 提出

---

<p align="center">
  ⭐ 如果这个 Skill 对你有帮助，请在 ClawHub 上点个星！<br>
  ⭐ If this skill helps you, please star it on ClawHub!
</p>
