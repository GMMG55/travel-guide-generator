# 三个完整案例

这些文件用于体验产品，采用历史日期或说明性预算，不是当前出行建议。下载 HTML 后用浏览器打开即可；GitHub 文件预览不会执行 HTML。当前没有已部署的在线示例站。

| 场景 | 行程 | HTML | 文字版 | 原始数据 |
| --- | --- | --- | --- | --- |
| 情侣海边休闲 | 青岛3天，2人总预算4000元 | [下载并打开](qingdao-couple.html) | [查看](qingdao-couple.md) | [JSON](qingdao-couple.json) |
| 亲子慢游 | 成都2天，2大1小总预算4500元 | [下载并打开](chengdu-family.html) | [查看](chengdu-family.md) | [JSON](chengdu-family.json) |
| 双人山水旅行 | 北京往返九寨沟5天，预算约8000元 | [下载并打开](jiuzhaigou-duo.html) | [查看](jiuzhaigou-duo.md) | [JSON](jiuzhaigou-duo.json) |

青岛与成都是说明性演示，部分行程没有地图坐标；九寨沟是2026年9月的历史生成案例，具体班次、天气和费用必须重新核实。数据校验通过只代表没有识别到结构或时间冲突，不代表完成了实地验证。

## 体验顺序

1. 打开任意 HTML，查看每天路线、餐饮、住宿、预算及天气备选。
2. 点击行程卡片右上角“编辑”，调整时间和费用，再点击“完成”。
3. 刷新后检查修改是否保留；修改只存于当前浏览器。
4. 使用页面中的打印/PDF或导出修改功能。页面导出修改为 JSON，附带的 ICS 与 GeoJSON 是初始行程快照，不会随本地编辑自动重建。

对应的 `.ics`、`.geojson`、`.normalized.json` 文件与 HTML 放在同一目录，使用同一文件名前缀。地图导出只包含有坐标的行程项。

## 复制提示词

### 青岛情侣

> 帮我生成青岛3天情侣休闲攻略，从北京出发，2人总预算4000元，要有海边、美食和下雨备选。出发日期是〔填写日期〕，不要太赶。

### 成都亲子

> 帮我生成成都2天亲子攻略，2大1小，预算4500元。出发日期是〔填写日期〕，孩子年龄是〔填写年龄〕，每天要午休、少步行，饮食清淡，下雨要有室内替代。

### 九寨沟双人

> 北京出发去九寨沟，2人5天4晚，总预算8000元，出发日期是〔填写日期〕。希望节奏轻松，留足转车时间，包含天气备选、住宿区域和每天预算。

## 本地重建

在仓库根目录运行，把 `qingdao-couple` 替换为另外一个案例名即可：

```bash
python scripts/build_guide.py examples/qingdao-couple.json --output-base examples/qingdao-couple
python scripts/validate_guide.py examples/qingdao-couple.normalized.json --strict
```

如果对你有帮助，欢迎 [Star 保存项目](https://github.com/GMMG55/travel-guide-generator)，或提交脱敏后的生成结果与问题。
