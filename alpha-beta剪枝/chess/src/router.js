import Vue from "vue";
import Router from "vue-router";
import Chess from "./views/Chess.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "chess",
      component: Chess
    }
  ]
});
