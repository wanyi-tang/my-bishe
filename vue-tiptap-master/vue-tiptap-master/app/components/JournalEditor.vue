<template>
  <div class="journal-workspace">
    <!-- Left Panel: Book Information -->
    <div class="left-panel">
      <div v-if="selectedBook" class="book-info-card">
        <h3>当前书籍</h3>
        <div class="book-cover-large">
          <img
            :src="
              selectedBook.cover ||
              'https://via.placeholder.com/200x300?text=No+Cover'
            "
            :alt="selectedBook.title"
          />
        </div>
        <div class="book-details">
          <h4>{{ selectedBook.title }}</h4>
          <p class="author">作者：{{ selectedBook.author }}</p>
          <p v-if="selectedBook.genre" class="genre">
            {{ selectedBook.genre }}
          </p>
        </div>
        <div class="book-stats">
          <div class="stat">
            <span class="stat-number">{{ bookJournals.length }}</span>
            <span class="stat-label">笔记数量</span>
          </div>
        </div>
      </div>
      <div v-else class="no-book-selected">
        <p>请从书架或下拉菜单中选择一本书开始写手账。</p>
      </div>

      <!-- Book Selector -->
      <div class="book-selector">
        <label for="book-select">切换书籍：</label>
        <select id="book-select" v-model="selectedBookId">
          <option value="">请选择书籍</option>
          <option v-for="book in books" :key="book.id" :value="book.id">
            {{ book.title }}（{{ book.author }}）
          </option>
        </select>
      </div>
    </div>

    <!-- Main Area: Rich Text Editor -->
    <div class="main-editor">
      <div class="editor-header">
        <h2>阅读手账</h2>
        <div class="editor-actions">
          <input
            v-model="currentTags"
            placeholder="添加标签（用逗号分隔）"
            class="tags-input"
          />
          <button
            @click="saveJournal"
            class="save-btn"
            :disabled="!currentContent.trim()"
          >
            保存笔记
          </button>
        </div>
      </div>

      <div class="editor-container">
        <Editor
          :initial-content="currentContent"
          :active-buttons="[
            'bold',
            'italic',
            'strike',
            'underline',
            'code',
            'h1',
            'h2',
            'h3',
            'bulletList',
            'orderedList',
            'blockquote',
            'codeBlock',
            'horizontalRule',
            'image',
            'undo',
            'redo',
          ]"
          @update="updateContent"
          placeholder="开始记录你的阅读心得..."
        />
      </div>
    </div>

    <!-- Right Panel: Notes List and Tags -->
    <div class="right-panel">
      <div class="panel-section">
        <h3>最近笔记</h3>
        <div class="notes-list">
          <div
            v-for="journal in bookJournals"
            :key="journal.id"
            class="note-item"
            @click="loadJournal(journal)"
            :class="{ active: currentJournalId === journal.id }"
          >
            <div class="note-preview">
              <p class="note-date">{{ formatDate(journal.date) }}</p>
              <p class="note-content">{{ getNotePreview(journal.content) }}</p>
            </div>
            <div v-if="journal.tags && journal.tags.length" class="note-tags">
              <span
                v-for="tag in journal.tags.slice(0, 3)"
                :key="tag"
                class="tag"
              >
                {{ tag }}
              </span>
              <span v-if="journal.tags.length > 3" class="tag more"
                >+{{ journal.tags.length - 3 }}</span
              >
            </div>
          </div>
          <div v-if="bookJournals.length === 0" class="empty-notes">
            <p>还没有笔记，开始写第一条阅读手账吧！</p>
          </div>
        </div>
      </div>

      <div class="panel-section">
        <h3>标签云</h3>
        <div class="tags-cloud">
          <span
            v-for="tag in allTags"
            :key="tag.name"
            class="tag-cloud-item"
            :style="{ fontSize: tag.size + 'px' }"
            @click="filterByTag(tag.name)"
          >
            {{ tag.name }} ({{ tag.count }})
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useBookStore } from '../stores/books.js';
import { useJournalStore } from '../stores/journals.js';
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, onBeforeRouteUpdate } from 'vue-router';
import Editor from './Editor.vue';

export default {
  name: 'JournalEditor',
  components: {
    Editor,
  },
  setup() {
    const bookStore = useBookStore();
    const journalStore = useJournalStore();
    const route = useRoute();

    const selectedBookId = ref('');
    const currentContent = ref('');
    const currentTags = ref('');
    const currentJournalId = ref(null);

    onMounted(() => {
      // Check if bookId is provided in query parameters
      const bookId = route.query.bookId;
      if (bookId && bookStore.books.some((book) => book.id == bookId)) {
        selectedBookId.value = bookId;
      }
    });

    // Computed properties
    const books = computed(() => bookStore.books);
    const selectedBook = computed(() =>
      bookStore.books.find((book) => book.id == selectedBookId.value),
    );
    const bookJournals = computed(() => {
      if (!selectedBookId.value) return [];
      return journalStore.journals
        .filter((journal) => journal.bookId == selectedBookId.value)
        .sort((a, b) => new Date(b.date) - new Date(a.date)); // Most recent first
    });

    const allTags = computed(() => {
      if (!selectedBookId.value) return [];

      const tagCount = {};
      bookJournals.value.forEach((journal) => {
        if (journal.tags) {
          journal.tags.forEach((tag) => {
            tagCount[tag] = (tagCount[tag] || 0) + 1;
          });
        }
      });

      return Object.entries(tagCount)
        .map(([name, count]) => ({
          name,
          count,
          size: Math.min(14 + count * 2, 24), // Dynamic font size based on count
        }))
        .sort((a, b) => b.count - a.count);
    });

    // Watch for book changes
    watch(selectedBookId, (newId) => {
      if (newId) {
        // Reset to new note mode
        currentContent.value = '';
        currentTags.value = '';
        currentJournalId.value = null;
      }
    });

    onBeforeRouteUpdate((to) => {
      const newBookId = to.query.bookId;
      if (newBookId && bookStore.books.some((book) => book.id == newBookId)) {
        selectedBookId.value = newBookId;
      }
      currentContent.value = '';
      currentTags.value = '';
      currentJournalId.value = null;
    });

    const updateContent = (content) => {
      currentContent.value = content;
    };

    const saveJournal = () => {
      if (!selectedBookId.value || !currentContent.value.trim()) return;

      const journalData = {
        bookId: selectedBookId.value,
        content: currentContent.value,
        tags: currentTags.value
          .split(',')
          .map((t) => t.trim())
          .filter((t) => t),
      };

      if (currentJournalId.value) {
        // Update existing journal
        journalStore.updateJournal(currentJournalId.value, journalData);
      } else {
        // Create new journal
        journalStore.addJournal(journalData);
      }

      // Reset for new note
      currentContent.value = '';
      currentTags.value = '';
      currentJournalId.value = null;
    };

    const loadJournal = (journal) => {
      currentContent.value = journal.content || '';
      currentTags.value = journal.tags ? journal.tags.join(', ') : '';
      currentJournalId.value = journal.id;
    };

    const filterByTag = (tagName) => {
      // For now, just show an alert. Could be enhanced to filter notes
      alert(`按标签：${tagName} 筛选（暂未实现更复杂筛选）。`);
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return (
        date.toLocaleDateString() +
        ' ' +
        date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      );
    };

    const getNotePreview = (content) => {
      // Strip HTML tags and get first 100 characters
      const text = content.replace(/<[^>]*>/g, '').trim();
      return text.length > 100 ? text.substring(0, 100) + '...' : text;
    };

    return {
      books,
      selectedBook,
      selectedBookId,
      bookJournals,
      allTags,
      currentContent,
      currentTags,
      currentJournalId,
      updateContent,
      saveJournal,
      loadJournal,
      filterByTag,
      formatDate,
      getNotePreview,
    };
  },
};
</script>

<style scoped>
.journal-workspace {
  display: grid;
  grid-template-columns: 320px 1fr 320px;
  grid-template-areas: 'left main right';
  height: 100vh;
  gap: 25px;
  padding: 25px;
  background: linear-gradient(135deg, #f4e4bc 0%, #f9f6f0 50%, #e8dcc0 100%);
  font-family: 'Georgia', serif;
}

.left-panel {
  grid-area: left;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  padding: 25px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  overflow-y: auto;
}

.main-editor {
  grid-area: main;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.right-panel {
  grid-area: right;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  padding: 25px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  overflow-y: auto;
}

/* Left Panel Styles */
.book-info-card {
  margin-bottom: 35px;
}

.book-info-card h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 20px;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 8px;
}

.book-cover-large {
  text-align: center;
  margin-bottom: 20px;
}

.book-cover-large img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  box-shadow:
    0 6px 15px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(139, 115, 85, 0.1);
  border: 2px solid #e8dcc0;
}

.book-details h4 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #5d4e37;
  line-height: 1.4;
  font-weight: bold;
}

.author {
  margin: 0 0 10px 0;
  color: #8b7355;
  font-style: italic;
  font-size: 16px;
}

.genre {
  margin: 0;
  color: #a0865c;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.book-stats {
  margin-top: 25px;
  display: flex;
  justify-content: center;
}

.stat {
  text-align: center;
  background: linear-gradient(135deg, #f4e4bc 0%, #e8dcc0 100%);
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-number {
  display: block;
  font-size: 28px;
  font-weight: bold;
  color: #d4af37;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #8b7355;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.no-book-selected {
  text-align: center;
  color: #8b7355;
  font-style: italic;
  padding: 40px 20px;
}

.book-selector {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e8dcc0;
}

.book-selector label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #5d4e37;
  font-size: 14px;
}

.book-selector select {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e8dcc0;
  border-radius: 6px;
  font-size: 14px;
  background: #fefcf8;
  color: #5d4e37;
  font-family: 'Georgia', serif;
}

.book-selector select:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}

/* Main Editor Styles */
.editor-header {
  padding: 25px;
  border-bottom: 2px solid #e8dcc0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
}

.editor-header h2 {
  margin: 0;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 24px;
}

.editor-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.tags-input {
  padding: 10px 12px;
  border: 2px solid #e8dcc0;
  border-radius: 6px;
  font-size: 14px;
  width: 220px;
  background: #fefcf8;
  color: #5d4e37;
  font-family: 'Georgia', serif;
}

.tags-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}

.save-btn {
  padding: 10px 18px;
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  border: 2px solid #b8860b;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(212, 175, 55, 0.3);
}

.save-btn:disabled {
  background: #e8dcc0;
  border-color: #d4af37;
  color: #8b7355;
  cursor: not-allowed;
  transform: none;
}

.editor-container {
  flex: 1;
  padding: 25px;
  overflow-y: auto;
  background: #fefcf8;
}

/* Right Panel Styles */
.panel-section {
  margin-bottom: 35px;
}

.panel-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 18px;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 8px;
}

.notes-list {
  max-height: 350px;
  overflow-y: auto;
  padding-right: 10px;
}

.notes-list::-webkit-scrollbar {
  width: 6px;
}

.notes-list::-webkit-scrollbar-track {
  background: #f9f6f0;
  border-radius: 3px;
}

.notes-list::-webkit-scrollbar-thumb {
  background: #d4af37;
  border-radius: 3px;
}

.note-item {
  padding: 15px;
  border: 2px solid #e8dcc0;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
}

.note-item:hover {
  background: linear-gradient(135deg, #f9f6f0 0%, #f4e4bc 100%);
  border-color: #d4af37;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 115, 85, 0.15);
}

.note-item.active {
  background: linear-gradient(135deg, #f4e4bc 0%, #e8dcc0 100%);
  border-color: #d4af37;
  box-shadow: inset 0 2px 6px rgba(212, 175, 55, 0.2);
}

.note-date {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #8b7355;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.note-content {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #5d4e37;
  line-height: 1.5;
}

.note-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.tag.more {
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  color: #f9f6f0;
}

.empty-notes {
  text-align: center;
  padding: 50px 20px;
  color: #8b7355;
  font-style: italic;
}

.empty-notes p {
  font-size: 16px;
  margin: 0;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-cloud-item {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid #b8860b;
}

.tag-cloud-item:hover {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: scale(1.05);
  box-shadow: 0 2px 6px rgba(212, 175, 55, 0.3);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .journal-workspace {
    grid-template-columns: 280px 1fr 280px;
  }
}

@media (max-width: 768px) {
  .journal-workspace {
    grid-template-columns: 1fr;
    grid-template-areas: 'main' 'left' 'right';
    height: auto;
  }

  .left-panel,
  .right-panel {
    max-height: 350px;
  }

  .editor-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .tags-input {
    width: 100%;
  }

  .editor-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
}
</style>
