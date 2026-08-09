import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ItineraryView from '../views/ItineraryView.vue';
export default createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: HomeView },
        { path: '/itinerary', name: 'itinerary', component: ItineraryView },
    ],
});
