# 旅游攻略HTML设计规范

## 配色方案

### 主色调
- **主色**: `#667eea` → `#764ba2` (紫蓝渐变)
- **强调色**: `#f2719c` (粉红)
- **警告色**: `#faad14` (金黄)
- **成功色**: `#52c41a` (绿色)
- **危险色**: `#ff4d4f` (红色)

### 背景色
- **页面背景**: `#f5f5f5`
- **卡片背景**: `#ffffff`
- **渐变背景**: 
  - Day1: `#f6a085` → `#f2719c` (橙粉)
  - Day2: `#4facfe` → `#00f2fe` (蓝青)
  - Day3: `#a18cd1` → `#fbc2eb` (紫粉)
  - Day4: `#fddb92` → `#d1fdff` (黄青)

### 文字色
- **主文字**: `#333333`
- **次文字**: `#666666`
- **辅助文字**: `#888888`
- **禁用文字**: `#bbbbbb`

## 字体

### 字体族
```css
font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
```

### 字号规范
- **大标题**: `2.2em` (Hero标题)
- **标题**: `1.3em` (卡片标题)
- **小标题**: `1.2em` (区域标题)
- **正文**: `1em` (默认)
- **小字**: `0.88em` (描述文字)
- **辅助**: `0.82em` (标签、提示)

## 布局

### 容器
```css
max-width: 780px;
margin: 0 auto;
padding: 20px 16px 60px;
```

### 卡片
```css
background: #fff;
border-radius: 16px;
box-shadow: 0 2px 12px rgba(0,0,0,.06);
```

### 间距
- **大间距**: `24px` (卡片间)
- **中间距**: `16px` (区域内)
- **小间距**: `12px` (元素间)
- **微间距**: `8px` (紧凑元素)

## 组件样式

### 标签
```css
background: rgba(255,255,255,.2);
backdrop-filter: blur(6px);
color: #fff;
padding: 4px 14px;
border-radius: 20px;
font-size: .82em;
```

### 价格标签
```css
background: #fff3e0;
color: #e65100;
font-size: .75em;
padding: 1px 8px;
border-radius: 8px;
```

### 高德API标签
```css
background: linear-gradient(135deg, #667eea, #764ba2);
color: #fff;
font-size: .7em;
padding: 3px 10px;
border-radius: 8px;
box-shadow: 0 2px 8px rgba(102,126,234,.3);
```

### 浪漫提示
```css
background: linear-gradient(90deg, #fff5f5, #fff0fb);
border-radius: 10px;
border-left: 3px solid #f2719c;
color: #c06;
```

### 避坑提示
```css
background: #fffbe6;
border-radius: 10px;
border-left: 3px solid #faad14;
color: #ad6800;
```

## 响应式断点

### 平板 (768px)
- 容器padding: `16px 12px 40px`
- 标题字号: `1.5em`
- 网格列数: 1列
- 卡片padding: `16px`

### 手机 (375px)
- 容器padding: `12px`
- 标题字号: `1.3em`
- 标签字号: `0.68em`
- 图标尺寸: `34px`

## 图标使用

使用emoji作为图标，简洁直观：
- 🌊 海边
- 🏨 酒店
- 🍜 美食
- 🚗 交通
- 📸 拍照
- 💕 浪漫
- ⚠️ 避坑
- 🗺️ 地图
- 🚄 高铁
- ✈️ 飞机

## 动画效果

### 淡入动画
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### 过渡效果
```css
transition: all .3s ease;
```

## 无障碍设计

- 最小点击区域: `44px`
- 对比度: 文字与背景对比度 ≥ 4.5:1
- 触摸优化: `-webkit-tap-highlight-color: transparent`
