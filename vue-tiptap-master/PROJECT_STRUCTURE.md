# 项目结构目录

## 根目录 (vue-tiptap-master)
```
vue-tiptap-master/
├── copilot_prompt.md          # Copilot 提示配置
├── package.json               # 项目依赖配置
├── README_DEV.md              # 开发者说明文档
├── vue-tiptap-master/         # 主项目目录
│   ├── eslint.config.js       # ESLint 配置
│   ├── index.html             # HTML 入口文件
│   ├── LICENSE.md             # 许可证
│   ├── package.json           # 项目依赖配置
│   ├── readme.md              # 项目说明文档
│   ├── vite.config.js         # Vite 构建配置
│   │
│   ├── app/                   # 应用主目录
│   │   ├── App.vue            # 根组件
│   │   ├── main.js            # 应用入口文件
│   │   ├── router.js          # 路由配置
│   │   │
│   │   ├── assets/            # 静态资源
│   │   │   └── icons/         # 图标资源
│   │   │
│   │   ├── components/        # Vue 组件
│   │   │   ├── AddBookDialog.vue      # 添加书籍对话框
│   │   │   ├── BookCard.vue           # 书籍卡片组件
│   │   │   ├── BookFilter.vue         # 书籍过滤组件
│   │   │   ├── BookFilterPanel.vue    # 书籍过滤面板
│   │   │   ├── BookManagement.vue     # 书籍管理组件
│   │   │   ├── Bookshelf.vue          # 书架组件
│   │   │   ├── Editor.vue             # 编辑器组件
│   │   │   ├── FilterPanel.vue        # 过滤面板
│   │   │   ├── HomePage.vue           # 首页组件
│   │   │   ├── Icon.vue               # 图标组件
│   │   │   ├── InlineSvg.vue          # 内联 SVG 组件
│   │   │   ├── JournalEditor.vue      # 日志编辑器组件
│   │   │   ├── StatisticsDashboard.vue # 统计仪表板
│   │   │   └── TagSystem.vue          # 标签系统组件
│   │   │
│   │   ├── router/            # 路由模块
│   │   │   └── index.js       # 路由索引
│   │   │
│   │   ├── sass/              # SCSS 样式文件
│   │   │   ├── editor.scss    # 编辑器样式
│   │   │   ├── icon.scss      # 图标样式
│   │   │   ├── main.scss      # 主样式
│   │   │   ├── menubar.scss   # 菜单栏样式
│   │   │   ├── menububble.scss # 菜单气泡样式
│   │   │   └── variables.scss # 样式变量
│   │   │
│   │   └── stores/            # Pinia/Vuex 状态管理
│   │       ├── books.js       # 书籍状态
│   │       └── journals.js    # 日志状态
│   │
│   ├── dist-example/          # 示例构建输出
│   │   ├── index.html
│   │   └── assets/            # 构建后的资源文件
│   │       ├── index-BJs2zZpP.js
│   │       ├── index-CRoJAHVv.js
│   │       ├── index-IRTLy4pR.css
│   │       └── index-UM1fjyBv.css
│   │
│   ├── img/                   # 图片资源
│   │
│   └── src/                   # 源代码目录（库版本）
│       ├── index.js           # 库入口文件
│       │
│       ├── assets/            # 静态资源
│       │   └── icons/         # 图标资源
│       │
│       ├── components/        # 组件目录
│       │   ├── Editor.vue     # 编辑器组件
│       │   ├── Icon.vue       # 图标组件
│       │   └── InlineSvg.vue  # 内联 SVG 组件
│       │
│       └── sass/              # SCSS 样式文件
│           ├── editor.scss    # 编辑器样式
│           ├── icon.scss      # 图标样式
│           ├── main.scss      # 主样式
│           ├── menubar.scss   # 菜单栏样式
│           ├── menububble.scss # 菜单气泡样式
│           └── variables.scss # 样式变量
```

## 主要功能模块说明

### 1. **核心组件** (`app/components/`)
- **编辑器相关**: `Editor.vue`, `JournalEditor.vue`
- **书籍管理**: `BookCard.vue`, `Bookshelf.vue`, `BookManagement.vue`
- **过滤系统**: `BookFilter.vue`, `BookFilterPanel.vue`, `FilterPanel.vue`
- **UI 组件**: `AddBookDialog.vue`, `Icon.vue`, `InlineSvg.vue`
- **页面组件**: `HomePage.vue`, `StatisticsDashboard.vue`, `TagSystem.vue`

### 2. **状态管理** (`app/stores/`)
- `books.js` - 书籍数据状态管理
- `journals.js` - 日志数据状态管理

### 3. **样式系统** (`app/sass/`)
- 采用 SCSS 预处理器
- 模块化设计：编辑器、图标、菜单栏等独立样式文件
- 统一变量管理 (`variables.scss`)

### 4. **路由系统** (`app/router/`)
- 使用 Vue Router 进行路由管理

### 5. **库源码** (`src/`)
- 包含可复用的编辑器核心组件
- 可作为独立库使用

## 技术栈
- **框架**: Vue.js
- **构建工具**: Vite
- **样式**: SCSS
- **状态管理**: Pinia/Vuex
- **富文本编辑器**: TipTap
- **代码规范**: ESLint
