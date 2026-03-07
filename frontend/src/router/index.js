import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Members from '../views/Events.vue';
import Learn from '../views/Learn.vue';
import Chat from '../views/Chat.vue';
import Register from '@/views/Register.vue';
import About from '../views/About.vue';
import Challenge from '../views/Challenge.vue';
import Executive from '../views/Executive.vue';
import ContactUs from '../views/ContactUs.vue';
import Profile from '../views/SetProfilePicture.vue';
import LogOut from '../views/LogOutView.vue';

function createPath(route,  component) {
  let comp;
  if (component) {
    comp = component;
  } else {
    comp = () => import(`../views/${component}.vue`);
  }
  return {
    path: `/${route}`,
    name: route.toLowerCase(),
    component: comp,
  }
}
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    createPath('members', Members),
    createPath('learn', Learn),
    createPath('chatroom', Chat),
    createPath('register', Register), 
    {
      path: '/aboutcms',
      name: 'aboutcms',
      component: About,
    },
      {
    path: '/learn/article/:id',
    name: 'Learn',
    component: () => import(`../views/Article.vue`),
    props: true // Automatically passes route params as props
  },
  createPath('executive', Executive),
  createPath('contactus', ContactUs),
  createPath('profile', Profile),
  createPath('logout', LogOut),
  ],
})

export default router
