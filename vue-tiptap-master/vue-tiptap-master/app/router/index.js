import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import JournalEditor from '../components/JournalEditor.vue';
import TagSystem from '../components/TagSystem.vue';
import StatisticsDashboard from '../components/StatisticsDashboard.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  {
    path: '/bookshelf',
    name: 'Bookshelf',
    component: () => import('../components/Bookshelf.vue'),
  },
  { path: '/editor', name: 'JournalEditor', component: JournalEditor },
  { path: '/tags', name: 'TagSystem', component: TagSystem },
  { path: '/stats', name: 'StatisticsDashboard', component: StatisticsDashboard },
  { path: '/:pathMatch(.*)*', redirect: '/' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
