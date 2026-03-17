<template>
  <div class="book-card" @click="$emit('click', book)">
    <div class="book-cover">
      <img :src="book.cover || defaultCover" :alt="book.title" @error="handleImageError" />
      <div class="hover-actions">
        <button @click.stop="$emit('edit', book)">编辑</button>
        <button class="delete" @click.stop="$emit('delete', book)">删除</button>
      </div>
    </div>
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-author">作者：{{ book.author }}</p>
      <p class="book-genre">{{ book.genre }} | {{ book.theme || '题材未设' }}</p>
      <div class="book-tags" v-if="book.tags && book.tags.length">
        <span v-for="tag in book.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
        <span v-if="book.tags.length > 3" class="tag more">+{{ book.tags.length - 3 }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookCard',
  props: {
    book: { type: Object, required: true },
  },
  emits: ['click', 'edit', 'delete'],
  data() {
    return {
      defaultCover: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="300" viewBox="0 0 200 300"%3E%3Crect width="200" height="300" fill="%23e5d8b5"/%3E%3Ctext x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="16" fill="%23907e4f" font-family="Arial, sans-serif"%3ENo Cover%3C/text%3E%3C/svg%3E',
    };
  },
  methods: {
    handleImageError(event) {
      event.target.src = this.defaultCover;
    },
  },
};
</script>

<style scoped>
.book-card {
  position: relative;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(139, 115, 85, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  overflow: hidden;
  transition: all 0.25s ease;
  cursor: pointer;
}
.book-card:hover { transform: translateY(-6px); box-shadow: 0 8px 20px rgba(139, 115, 85, 0.2); }
.book-cover { height: 200px; position: relative; overflow: hidden; }
.book-cover img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.book-card:hover .book-cover img { transform: scale(1.05); }
.hover-actions {
  position: absolute; bottom: 10px; right: 10px; display: flex; gap: 6px; opacity: 0; transition: opacity 0.2s ease;
}
.book-card:hover .hover-actions { opacity: 1; }
.hover-actions button { border: 1px solid #f0f0f0; background: rgba(0, 0, 0, 0.5); color: #fff; font-size: 12px; border-radius: 4px; padding: 4px 8px; cursor: pointer; }
.hover-actions .delete { background: rgba(185, 33, 33, 0.9); }
.book-info { padding: 14px; }
.book-title { margin: 0 0 8px; font-size: 18px; color: #4d3928; font-weight: bold; font-family:'Georgia', serif; }
.book-author { margin: 0 0 6px; color: #7e6545; font-size: 14px; }
.book-genre { margin: 0 0 10px; color: #a0865c; font-size: 13px; font-weight: 600; }
.book-tags { display: flex; flex-wrap: wrap; gap: 5px; }
.tag { background: #d4af37; color: #fff; border-radius: 999px; padding: 3px 8px; font-size: 11px; }
.tag.more { background: #8b7355; }
</style>
