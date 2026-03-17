<template>
  <div id="app">
    <nav>
      <router-link to="/">首页</router-link>
      <router-link to="/bookshelf">书架</router-link>
      <router-link to="/editor">手账编辑</router-link>
      <router-link to="/tags">标签系统</router-link>
      <router-link to="/stats">阅读统计</router-link>
    </nav>
    <router-view :key="$route.fullPath" />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style lang="scss">
@use './sass/main.scss' as *;
</style>

<style lang="css">
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #f4e4bc 0%, #f9f6f0 50%, #e8dcc0 100%);
  background-attachment: fixed;
  font-family: 'Georgia', 'Times New Roman', serif;
  color: #5d4e37;
}

#app * {
  box-sizing: border-box;
}

nav {
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  box-shadow: 0 2px 10px rgba(139, 115, 85, 0.3);
  border-bottom: 2px solid #6b5b47;
  padding: 0;
  display: flex;
  justify-content: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

nav a {
  color: #f9f6f0;
  text-decoration: none;
  padding: 15px 25px;
  display: block;
  font-weight: 500;
  font-size: 16px;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  position: relative;
}

nav a:hover {
  background: rgba(249, 246, 240, 0.1);
  color: #fff;
}

nav a.router-link-active {
  background: linear-gradient(135deg, #6b5b47 0%, #8b7355 100%);
  color: #fff;
}

nav a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: #d4af37;
  border-radius: 2px;
}

/* Paper texture overlay */
#app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(
      circle at 25% 25%,
      rgba(139, 115, 85, 0.02) 2px,
      transparent 2px
    ),
    radial-gradient(
      circle at 75% 75%,
      rgba(139, 115, 85, 0.02) 2px,
      transparent 2px
    );
  background-size: 40px 40px;
  pointer-events: none;
  z-index: -1;
}
</style>
