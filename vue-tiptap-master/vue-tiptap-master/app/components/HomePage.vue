<template>
  <div class="home-page">
    <div class="home-header">
      <h1>阅读笔记学院</h1>
      <p>欢迎回来！从下面四个模块快速进入你的读书与手账空间。</p>
    </div>
    <div class="modules-grid">
      <router-link to="/bookshelf" class="module-card">
        <div class="module-icon">📚</div>
        <h3>我的书架</h3>
        <p>新增、编辑、筛选你的阅读书目。</p>
      </router-link>
      <router-link to="/editor" class="module-card">
        <div class="module-icon">📝</div>
        <h3>阅读手账</h3>
        <p>为当前书籍写读书笔记并管理标签。</p>
      </router-link>
      <router-link to="/tags" class="module-card">
        <div class="module-icon">🏷️</div>
        <h3>标签管理</h3>
        <p>查看所有标签并按标签筛选笔记。</p>
      </router-link>
      <router-link to="/stats" class="module-card">
        <div class="module-icon">📊</div>
        <h3>阅读统计</h3>
        <p>查看阅读趋势、笔记数量和题材分布。</p>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
.home-page {
  min-height: calc(100vh - 80px);
  padding: 32px;
  background: linear-gradient(135deg, #f4e4bc 0%, #f9f6f0 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #5d4e37;
}
.home-header {
  text-align: center;
  max-width: 860px;
  margin-bottom: 26px;
  border-radius: 14px;
  background: #fff8e6;
  padding: 20px 24px;
  border: 1px solid #d9c188;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}
.home-header h1 {
  margin: 0;
  font-size: 2.2rem;
  font-family: 'Georgia', serif;
  color: #5d4e37;
}
.home-header p {
  margin: 10px 0 0;
  color: #7b6447;
  font-size: 1rem;
}
.modules-grid {
  width: 100%;
  max-width: 1000px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
}
.module-card {
  background: #fff8e6;
  border-radius: 12px;
  border: 1px solid #e4d2a1;
  color: #5d4e37;
  text-decoration: none;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.module-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.14);
}
.module-icon {
  font-size: 2rem;
}
.module-card h3 {
  margin: 0;
  font-size: 1.2rem;
  font-family: 'Georgia', serif;
  color: #5d4e37;
}
.module-card p {
  margin: 0;
  color: #7b6447;
  font-size: 0.95rem;
  line-height: 1.4;
}
</style>