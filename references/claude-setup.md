# 在 Claude 中使用

本项目是独立第三方 Agent Skill，未被 Anthropic 官方收录或背书。Anthropic Skills 机制、ClawHub 分发平台和第三方安装工具是不同渠道；安装不代表进入官方榜单或公开下载统计。

## 推荐：使用 npx 安装

安装 Node.js 后，在目标项目目录运行，交互选择需要安装到的环境：

```bash
npx skills add GMMG55/travel-guide-generator
```

指定 Claude Code：

```bash
npx skills add GMMG55/travel-guide-generator --skill travel-guide-generator -a claude-code
```

指定 Codex：

```bash
npx skills add GMMG55/travel-guide-generator --skill travel-guide-generator -a codex
```

默认安装到当前项目。希望跨项目使用时加 `-g`，例如全局安装到 Claude Code：

```bash
npx skills add GMMG55/travel-guide-generator --skill travel-guide-generator -a claude-code -g
```

`npx skills` 是 Vercel 维护的第三方安装工具，与 Anthropic 的 Skills 机制配合使用；不是 Anthropic 官方安装器。Node.js 用于安装，生成攻略的脚本还需要 Python 3.8+。无需手动克隆、打包和解压即可走此安装路径。

安装后，Claude Code 使用 `/travel-guide-generator` 加旅行需求，Codex 可在对话中使用 `$travel-guide-generator` 加需求。若当前会话尚未发现技能，重新启动会话后检查。联网搜索由实际宿主提供。

## Prompt 安装：让 AI 执行安装

将以下 Prompt 发送给具备终端和联网权限的 Claude Code 或 Codex：

```text
请帮我安装这个旅行攻略 Skill：
https://github.com/GMMG55/travel-guide-generator

先检查当前使用的 Agent 和 Node.js 环境，阅读仓库的 SKILL.md，
再通过 npx skills add GMMG55/travel-guide-generator 安装到当前项目对应的 Agent。
如果已经安装，请先检查版本与本地修改，不要直接覆盖。
安装后检查技能是否能被发现，并告诉我如何调用；不要自动生成旅行攻略。
```

这是让 Agent 代为执行上面的 npx 安装流程，不是新的安装器。默认安装到当前项目；需要全局使用时补充“请全局安装”。如果缺少 Node.js，让 Agent 说明缺失项和安装方法，不要把依赖缺失当成技能安装成功。

安装验证应区分“文件已安装”“当前会话能发现技能”和“实际运行成功”。如果需要重启会话，明确提示；不能仅凭命令已执行就声称全流程验证通过。Claude 网页端按后文的 ZIP 上传流程操作，不能假设对话有权限修改用户电脑的技能目录。

## 手动安装（备选）：Claude Code 技能目录

把完整技能目录放到 `~/.claude/skills/travel-guide-generator/`，其中必须直接包含 `SKILL.md`。项目级安装使用 `.claude/skills/travel-guide-generator/`。

不能使用 npx 或希望自行检查安装文件时，可从本地生成的最小安装 ZIP 解压安装，避免复制 `.git`、测试产物和个人配置：

```bash
git clone https://github.com/GMMG55/travel-guide-generator.git
cd travel-guide-generator
python3 scripts/package_skill.py
```

macOS / Linux：

```bash
mkdir -p ~/.claude/skills
unzip -n dist/travel-guide-generator.zip -d ~/.claude/skills
```

Windows PowerShell（在克隆后的仓库目录运行）：

```powershell
python scripts/package_skill.py
$skillTarget = Join-Path $env:USERPROFILE '.claude\skills'
New-Item -ItemType Directory -Path $skillTarget -Force | Out-Null
Expand-Archive -LiteralPath 'dist\travel-guide-generator.zip' -DestinationPath $skillTarget
```

若已安装同名目录，先检查并备份自己的修改后再更新，不要盲目覆盖。进入 Claude Code 后检查 `/` 菜单并运行：

```text
/travel-guide-generator 帮我规划北京出发的青岛3天情侣休闲游，2人总预算4000元，要有美食和下雨备选。先确认出发日期。
```

技能也可以按旅行规划需求自动加载。自然语言请求未触发时，使用完整命令名。模型调用方式与权限仍受本机 Claude Code 设置约束。

## Claude 网页端：上传 ZIP

1. 在仓库根目录运行 `python scripts/package_skill.py`，得到 `dist/travel-guide-generator.zip`。
2. 确认账户已启用代码执行和文件创建；组织账户还可能需要管理员启用 Skills。
3. 在 `Customize > Skills` 中选择添加自定义技能、上传 ZIP，并启用它。具体菜单以当前账户界面为准。
4. 在新对话中用自然语言请求生成攻略，并说明目的地、日期、人数、预算与节奏。
5. 下载生成的 HTML，使用浏览器打开；其他文件包括 Markdown、ICS、GeoJSON 和规范化 JSON。

不要上传 GitHub “Download ZIP” 原包代替技能安装包：原包含开发文档等非运行资源，而打包脚本只选择运行必需文件。

## 三步首次体验

安装并启用 → 发送完整旅行需求 → 下载 HTML 查看与编辑。

第一次不需要高德 API Key。Python 3.8+ 即可运行本地构建器；当前版本无第三方 Python 运行时依赖。实际攻略检索需要宿主提供网页搜索；无法联网也能生成带估算标记的示例。

## 脚本运行路径

Claude Code 中可按以下方式调用，输入与输出绝对路径替换成任务实际路径：

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_guide.py" /absolute/path/guide.json --output-base /absolute/path/output/trip
```

其他宿主从其实际技能安装路径调用同一脚本。构建会写入输出目录，不需要切换到技能目录，也不需要修改全局环境变量。

## 兼容性验证范围

| 项目 | 验证方式 | 状态 |
| --- | --- | --- |
| Agent Skills frontmatter | 本地格式校验 | 运行发布前校验，以结果为准 |
| ZIP 结构及资源 | 解压后检查文件和相对引用 | 本地打包流程可验证 |
| Python 生成与导出 | 从解压后的包调用构建器 | 本地可验证 |
| Claude Code 自动触发及命令 | 需在已登录 Claude Code 中人工实测 | 尚未实测 |
| Claude 网页端上传与附件下载 | 需在用户账户中人工实测 | 尚未实测 |

遇到问题时请反馈宿主名称/版本、操作系统、失败步骤和已脱敏报错。不要提交 Token、API Key 或个人行程中的敏感信息。

## 官方参考

- [Anthropic Skills 示例仓库](https://github.com/anthropics/skills)
- [Agent Skills 格式规范](https://agentskills.io/specification)
- [Claude Code Skills 文档](https://code.claude.com/docs/en/skills)
- [在 Claude 中启用和上传 Skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [第三方 Skills CLI 安装说明](https://github.com/vercel-labs/skills)

安装说明核对日期：2026-10-27。
