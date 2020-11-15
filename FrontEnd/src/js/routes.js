import Login from '../pages/login.vue';
import HomePage from '../pages/dash.vue';
import CardPage from '../pages/cards.vue';
import CameraView from '../pages/CameraView.vue'
import NotFoundPage from '../pages/404.vue';
import AboutPage from '../pages/about.vue'

var routes = [
  {
    path: '/',
    component: Login,
  },
  {
    path: '/home/',
    component: HomePage,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/camera/',
    component: CameraView,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/about/',
    component: AboutPage,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/cards/',
    component: CardPage,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '(.*)',
    component: NotFoundPage,
  },
];

export default routes;
