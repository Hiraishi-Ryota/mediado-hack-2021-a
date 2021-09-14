import Vue from 'vue'
import Router from 'vue-router'
import UploadTop from '@/pages/UploadTop'
import UploadConfirm from '@/pages/UploadConfirm'
import BookList from '@/pages/BookList'
import BookDetails from '@/pages/BookDetails'
import ReadScreen from '@/pages/ReadScreen'
import PurchasedList from '@/pages/PurchasedList'

Vue.use(Router)

export default new Router({
  mode: 'history', //追加
  routes: [
    {
      path: '/',
      component: UploadTop,
    },
    {
      path: '/upload_confirm',
      component: UploadConfirm,
    },
    {
      path: '/book_list',
      component: BookList,
    },
    {
      path: '/book_list/:id',
      component: BookDetails,
      props: true,
    },
    {
      path: '/read_screen/:id/:title',
      component: ReadScreen,
      props: true,
    },
    {
      path: '/purchased_list',
      component: PurchasedList,
    },
  ],
})
