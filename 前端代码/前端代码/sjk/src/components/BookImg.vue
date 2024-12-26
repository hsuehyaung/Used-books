<template>
  <div class="book-img">
    <h1>{{ book.book_name }}</h1>
    <p>ISBN: {{ book.ISBN }}</p>
    <p>Price: {{ book.price }}</p>
    <p>Sales: {{ book.m_sale_v }}</p>
    <img :src="book.book_img" alt="Book Cover" v-if="book.book_img">
    <!-- 可以在这里添加更多的图书信息展示 -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      book: {}
    };
  },
  created() {
    const bookName = this.$route.params.bookName;
    // 明确指定请求方法为GET
    this.$axios.get(`/api/user/book/${bookName}`)
      .then(response => {
        this.book = response.data;
      })
      .catch(error => {
        console.error("Error fetching book data:", error);
        // 可以在这里添加用户友好的错误处理，比如显示错误消息
        this.$message.error("Failed to load book data. Please try again later.");
      });
  }
};
</script>

<style scoped>
.book-img {
  margin: 20px;
  text-align: center;
  background: url('../assets/image/11.jpg'); /* 假设背景图片的路径为 '../assets/background.jpg'，可根据实际情况修改 */
  background-size: cover; /* 使背景图片覆盖整个元素 */
  background-repeat: no-repeat; /* 防止背景图片重复 */
  background-position: center; /* 将背景图片居中 */
}

.book-img img {
  max-width: 100%;
  height: auto; /* 保持图片比例 */
  margin-top: 20px; /* 可选，为图片添加顶部间距 */
}
</style>