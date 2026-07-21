# 每日行程卡片 HTML 规范

本文档详细说明每日行程卡片的HTML结构，包括两个新增模块。

## 基本结构

```html
<!-- Day1 卡片示例 -->
<div class="day-card">
  <div class="day-header d1">
    <div class="day-num">Day 1 · 浪漫启程</div>
    <div class="day-title">北京 → 威海 · 初见大海</div>
    <div class="day-route">威海公园 → 火炬八街 → 国际海水浴场</div>
  </div>
  
  <!-- 路线条 -->
  <div class="route-bar">
    <span class="dot"></span>
    <span class="r-item">威海公园</span>
    <span>→ 驾车 8.5km/20分钟 →</span>
    <span class="r-item">火炬八街</span>
    <span>→ 驾车 3.2km/10分钟 →</span>
    <span class="r-item">国际海水浴场</span>
  </div>
  
  <!-- 景点列表 -->
  <div class="spot">
    <div class="spot-head">
      <div class="spot-icon">🏞️</div>
      <div>
        <div class="spot-name">威海公园 <span class="spot-price">免费</span></div>
        <!-- [NEW] 第一个景点不显示交通提示 -->
        <div class="spot-desc">......</div>
      </div>
    </div>
    <div class="spot-romance">💕 浪漫时刻：......</div>
    <div class="pitfall">⚠️ 避坑：......</div>
  </div>
  
  <!-- 更多景点... -->
  
  <!-- 美食推荐 -->
  <div class="food-section" style="margin: 16px 24px; padding: 16px 20px;">
    <h2>🍽️ 晚餐推荐</h2>
    <div class="food-grid">
      <!-- 美食项... -->
    </div>
  </div>
  
  <!-- [NEW] 推荐酒店住宿地（仅需要住宿时显示） -->
  <div class="hotel-rec-section">
    <div class="hr-title">🏨 推荐酒店住宿地</div>
    <div class="hr-grid">
      <div class="hr-item">
        <div class="hr-name">威海公园附近酒店</div>
        <div class="hr-price">💰 300-500元/晚</div>
        <div class="hr-desc">推荐理由：离Day2首个景点近，节省路程时间。推荐酒店：XX酒店（海景房）、XX民宿（性价比高）</div>
      </div>
      <div class="hr-item">
        <div class="hr-name">火炬八街附近酒店</div>
        <div class="hr-price">💰 400-600元/晚</div>
        <div class="hr-desc">推荐理由：就在网红街旁，晚上可以散步拍照。推荐酒店：XX酒店（网红打卡）、XX民宿（ins风）</div>
      </div>
    </div>
    <div class="hr-tip">💡 衔接说明：推荐住威海公园附近，明天到火炬八街仅20分钟车程，方便开始Day2行程</div>
  </div>
  
</div>

<!-- Day2 卡片示例（包含新增的酒店→景点路线） -->
<div class="day-card">
  <div class="day-header d2">
    <div class="day-num">Day 2 · 浪漫海滨</div>
    <div class="day-title">威海深度游 · 情侣专属</div>
    <div class="day-route">酒店 → 火炬八街 → 猫头山 → 那香海</div>
  </div>
  
  <!-- [NEW] 酒店→景点路线条（Day2+ 开头） -->
  <div class="hotel-route-bar">
    <span class="hdot"></span>
    <span class="hroute-item">🏨 威海公园附近酒店</span>
    <span>→ 驾车 8.5km/20分钟 →</span>
    <span class="hroute-item">📍 火炬八街（Day2首个景点）</span>
  </div>
  
  <!-- 路线条 -->
  <div class="route-bar">
    <span class="dot"></span>
    <span class="r-item">火炬八街</span>
    <span>→ 驾车 12km/25分钟 →</span>
    <span class="r-item">猫头山</span>
    <span>→ 驾车 18km/30分钟 →</span>
    <span class="r-item">那香海</span>
  </div>
  
  <!-- 景点列表 -->
  <div class="spot">
    <div class="spot-head">
      <div class="spot-icon">📍</div>
      <div>
        <div class="spot-name">火炬八街 <span class="spot-price">免费</span></div>
        <!-- [NEW] 景点间交通提示（从上一个地点到这里） -->
        <span class="spot-transit"><span class="transit-icon">🚗</span> 从威海公园出发 · 驾车 <span class="transit-time">8.5km/20分钟</span></span>
        <div class="spot-desc">......</div>
      </div>
    </div>
    <div class="spot-romance">💕 浪漫时刻：......</div>
    <div class="pitfall">⚠️ 避坑：......</div>
  </div>
  
  <!-- 更多景点... -->
  
</div>
```

## 三个新增模块详解

### 1. 景点间交通提示（`.spot-transit`）

**显示位置**：每个景点名称行右侧（`.spot-name` 内部或紧跟其后）
**显示条件**：第一个景点不显示；从第二个景点开始，每个都显示从前一地点到这里的交通方式和时间
**内容结构**：
- 交通图标（🚗驾车 / 🚶步行 / 🚇地铁 / 🚌公交）
- 出发地名称
- 距离 + 用时

**HTML结构**：
```html
<span class="spot-transit"><span class="transit-icon">🚗</span> 从上一景点名出发 · 驾车 <span class="transit-time">XXkm/XX分钟</span></span>
```

**注意**：
- Day2+ 的第一个景点，出发地应为前一晚酒店名称
- Day1 的第一个景点不显示此提示
- 交通方式根据实际情况选择（驾车/步行/地铁/公交/打车）
- 如果高德API可用，距离和时间使用实测数据

### 2. 推荐酒店住宿地模块（`.hotel-rec-section`）

**显示位置**：每日行程卡片内部，晚餐美食推荐下方  
**显示条件**：仅当需要住宿时（非当日往返）  
**内容结构**：
- 标题：🏨 推荐酒店住宿地
- 酒店网格（2列）：酒店区域名称、价格区间、推荐理由
- 衔接说明：与次日行程的衔接说明

**HTML结构**：
```html
<div class="hotel-rec-section">
  <div class="hr-title">🏨 推荐酒店住宿地</div>
  <div class="hr-grid">
    <div class="hr-item">
      <div class="hr-name">酒店区域名称</div>
      <div class="hr-price">💰 价格区间</div>
      <div class="hr-desc">推荐理由：......</div>
    </div>
    <!-- 更多酒店项... -->
  </div>
  <div class="hr-tip">💡 衔接说明：......</div>
</div>
```

### 3. 酒店→景点路线条模块（`.hotel-route-bar`）

**显示位置**：Day2及以后每天的路线条（`.route-bar`）最前面  
**显示条件**：每天需要住宿时（即不是第一天）  
**内容结构**：
- 酒店名称（前一晚住宿地）
- → 驾车 XXkm/XX分钟 →
- 当日首个景点名称

**HTML结构**：
```html
<div class="hotel-route-bar">
  <span class="hdot"></span>
  <span class="hroute-item">🏨 酒店名称</span>
  <span>→ 驾车 XXkm/XX分钟 →</span>
  <span class="hroute-item">📍 首个景点名称</span>
</div>
```

## 数据填充说明

两个新模块的数据需要从以下内容中获取：

1. **酒店住宿推荐**：从搜索的攻略内容中提取酒店区域、价格、推荐理由
2. **酒店→景点路线**：需要前一晚酒店位置 + 当日首个景点位置，使用高德API计算距离和用时

## 高德API使用说明

用于计算景点间距离和用时，无需地图显示功能：

1. **路线规划API**：`https://restapi.amap.com/v3/direction/driving`（计算酒店→景点路线）
2. **地理编码API**：`https://restapi.amap.com/v3/geocode/geo`（获取景点坐标）

详见 `scripts/amap_route.py`。
