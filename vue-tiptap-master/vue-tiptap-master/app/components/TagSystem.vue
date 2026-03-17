<template>
  <div class="tag-system">
    <h2>标签管理</h2>

    <div class="tag-section">
      <h3>所有标签</h3>
      <ul v-if="allTags.length > 0">
        <li v-for="tag in allTags" :key="tag" class="tag-item">
          <span class="tag-name">{{ tag }}</span>
          <span class="tag-count">{{ getTagCount(tag) }} 条笔记</span>
        </li>
      </ul>
      <div v-else class="empty-state">
        <p>
          当前还没有标签。写一些带标签的手账笔记后这里会显示。
        </p>
      </div>
    </div>

    <div class="tag-section">
      <h3>按标签筛选笔记</h3>
      <select v-model="selectedTag">
        <option value="">选择标签</option>
        <option v-for="tag in allTags" :key="tag" :value="tag">
          {{ tag }}
        </option>
      </select>

      <ul v-if="selectedTag && journalsByTag.length > 0">
        <li
          v-for="journal in journalsByTag"
          :key="journal.id"
          class="journal-item"
        >
          <div class="book-title">{{ getBookTitle(journal.bookId) }}</div>
          <div class="journal-preview">
            {{ getJournalPreview(journal.content) }}
          </div>
        </li>
      </ul>

      <div v-else-if="selectedTag" class="empty-state">
        <p>未找到包含此标签的笔记。</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useJournalStore } from '../stores/journals.js';
import { useBookStore } from '../stores/books.js';
import { ref, computed } from 'vue';
import { onBeforeRouteUpdate } from 'vue-router';

export default {
  name: 'TagSystem',
  setup() {
    const journalStore = useJournalStore();
    const bookStore = useBookStore();
    const selectedTag = ref('');

    const allTags = computed(() => {
      const tags = new Set();
      journalStore.journals.forEach((journal) => {
        journal.tags.forEach((tag) => tags.add(tag));
      });
      return Array.from(tags);
    });

    const journalsByTag = computed(() => {
      if (!selectedTag.value) return [];
      return journalStore.journals.filter((journal) =>
        journal.tags.includes(selectedTag.value),
      );
    });

    const getTagCount = (tag) => {
      return journalStore.journals.filter((journal) =>
        journal.tags.includes(tag),
      ).length;
    };

    const getBookTitle = (bookId) => {
      const book = bookStore.getBookById(bookId);
      return book ? book.title : 'Unknown Book';
    };

    const getJournalPreview = (content) => {
      // Strip HTML tags and get first 150 characters
      const text = content.replace(/<[^>]*>/g, '').trim();
      return text.length > 150 ? text.substring(0, 150) + '...' : text;
    };

    onBeforeRouteUpdate(() => {
      selectedTag.value = '';
    });

    return {
      allTags,
      selectedTag,
      journalsByTag,
      getTagCount,
      getBookTitle,
      getJournalPreview,
    };
  },
};
</script>

<style scoped>
.tag-system {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px;
  background: linear-gradient(135deg, #f4e4bc 0%, #f9f6f0 50%, #e8dcc0 100%);
  min-height: 100vh;
  font-family: 'Georgia', serif;
}

.tag-system h2 {
  text-align: center;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 32px;
  margin-bottom: 40px;
  border-bottom: 3px solid #d4af37;
  padding-bottom: 15px;
  display: inline-block;
  width: 100%;
}

.tag-system h3 {
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 24px;
  margin-bottom: 20px;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 8px;
}

.tag-section {
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  padding: 25px;
  margin-bottom: 30px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tag-item {
  background: linear-gradient(135deg, #f4e4bc 0%, #e8dcc0 100%);
  border-radius: 8px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 15px 20px;
  margin: 8px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.tag-item:hover {
  transform: translateY(-2px);
  box-shadow:
    0 4px 12px rgba(139, 115, 85, 0.2),
    inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tag-name {
  font-size: 18px;
  color: #5d4e37;
  font-weight: bold;
}

.tag-count {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
}

select {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #e8dcc0;
  border-radius: 6px;
  font-size: 16px;
  background: #fefcf8;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

select:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}

.journal-item {
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 8px;
  box-shadow:
    0 2px 10px rgba(139, 115, 85, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  padding: 15px;
  margin: 8px 0;
  transition: all 0.3s ease;
}

.journal-item:hover {
  transform: translateY(-1px);
  box-shadow:
    0 4px 15px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.book-title {
  color: #5d4e37;
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 5px;
}

.journal-preview {
  color: #8b7355;
  font-size: 14px;
  line-height: 1.4;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #8b7355;
  font-style: italic;
}

.empty-state p {
  font-size: 18px;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .tag-system {
    padding: 20px;
  }

  .tag-system h2 {
    font-size: 28px;
  }

  .tag-section {
    padding: 20px;
  }

  .tag-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .tag-count {
    align-self: flex-end;
  }
}
</style>
