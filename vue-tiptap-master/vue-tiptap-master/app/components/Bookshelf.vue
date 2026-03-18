<template>
  <div class="bookshelf-page">
    <div class="page-header">
      <h1>我的个人书架</h1>
      <p>发现、整理并记录您的阅读冒险</p>
    </div>

    <div class="toolbar">
      <input
        class="search-input"
        v-model="search"
        @input="bookStore.setSearchQuery(search)"
        placeholder="搜索书名..."
      />
      <!-- <button class="add-book-btn" @click="openAddDialog">+ 添加书籍</button> -->
      <button class="clear-filters-btn" @click="clearFilters">清空筛选</button>
    </div>

    <div class="content-layout">
      <aside class="filter-sidebar">
        <BookFilterPanel
          :genres="allGenres"
          :themes="allThemes"
          :tags="allTags"
          :selected-genres="selectedGenres"
          :selected-themes="selectedThemes"
          :selected-tags="selectedTags"
          @update:selectedGenres="bookStore.updateSelectedGenres"
          @update:selectedThemes="bookStore.updateSelectedThemes"
          @update:selectedTags="bookStore.updateSelectedTags"
          @add-genre="addGenre"
          @add-theme="addTheme"
          @add-tag="addTag"
          @remove-genre="removeGenre"
          @remove-theme="removeTheme"
          @remove-tag="removeTag"
          @clear="clearFilters"
        />
      </aside>
      <main class="bookshelf-main">
        <div class="bookshelf-header">
          <div class="header-info">
            <h2>
              {{ totalBooks }} 本书
            </h2>
            <!-- <p style="font-size: 12px; color: #5d4e37;">调试：visibleBooks = {{ visibleBooks.length }}</p> -->
          </div>
          <button @click="openAddDialog" class="add-book-btn">添加书籍</button>
        </div>
        <!-- <pre style="background:#fff; color:#222; border:1px solid #ccc; padding:8px; margin:8px 0; overflow:auto;">{{ bookStore.books }}</pre> -->
        <div class="bookshelf-grid" v-if="filteredBooks.length > 0">
          <BookCard
            v-for="book in filteredBooks"
            :key="book.id"
            :book="book"
            @click="openDetail(book)"
            @edit="openEdit(book)"
            @delete="confirmDelete(book)"
          />
        </div>
        <div v-else class="empty-bookshelf">
          <div class="empty-content">
            <h3>{{ hasAnyFilter ? '暂无符合筛选的书籍' : '当前书架暂无书籍' }}</h3>
            <p>{{ hasAnyFilter ? '请调整筛选条件后重试。' : '可以先添加第一本书。' }}</p>
            <div class="empty-actions">
              <button class="add-first-book-btn" @click="openAddDialog">添加书籍</button>
            </div>
          </div>
        </div>
      </main>
    </div>

    <AddBookDialog
      :show="showAddBookModal"
      :mode="addMode"
      :book="editingBook"
      @close="closeDialog"
      @saved="closeDialog"
    />

    <!-- Book Detail Modal -->
    <div
      v-if="selectedBook"
      class="modal-overlay"
      @click="closeBookDetailModal"
    >
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedBook.title }}</h2>
          <button @click="closeBookDetailModal" class="close-btn">
            &times;
          </button>
        </div>

        <div class="modal-content">
          <div class="book-detail-layout">
            <div class="book-cover-large">
              <img
                :src="
                  selectedBook.cover ||
                  'https://via.placeholder.com/300x450?text=No+Cover'
                "
                :alt="selectedBook.title"
                @error="handleImageError"
              />
            </div>

            <div class="book-details">
              <div class="detail-section">
                <h3>作者</h3>
                <p>{{ selectedBook.author }}</p>
              </div>

              <div class="detail-section">
                <h3>文学题材</h3>
                <p>{{ selectedBook.genre }}</p>
              </div>

              <div class="detail-section" v-if="selectedBook.description">
                <h3>描述</h3>
                <p>{{ selectedBook.description }}</p>
              </div>

              <div
                class="detail-section"
                v-if="selectedBook.tags && selectedBook.tags.length"
              >
                <h3>标签</h3>
                <div class="tags-list">
                  <span
                    v-for="tag in selectedBook.tags"
                    :key="tag"
                    class="tag"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="openJournal" class="journal-btn">打开日志</button>
          <button @click="deleteBook" class="delete-btn">删除</button>
          <button @click="closeBookDetailModal" class="close-modal-btn">
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useBookStore } from '../stores/books.js';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { computed, ref, watch, onMounted } from 'vue';
import BookCard from './BookCard.vue';
import BookFilterPanel from './BookFilterPanel.vue';
import AddBookDialog from './AddBookDialog.vue';
export default {
  name: 'Bookshelf',
  components: {
    BookCard,
    BookFilterPanel,
    AddBookDialog,
  },
  setup() {
    onMounted(async () => {
      await bookStore.fetchBooks();
    });
    const bookStore = useBookStore();
    const { books, allGenres, allThemes, allTags, selectedGenres, selectedThemes, selectedTags } = storeToRefs(bookStore);
    const router = useRouter();

    const search = ref(bookStore.searchQuery || '');
    const authorQuery = ref('');
    const showAddBookModal = ref(false);
    const selectedBook = ref(null);
    const editingBook = ref(null);
    const addMode = ref('add');

    const filteredBooks = computed(() => {
      return books.value.filter((book) => {
        const authorMatch = !authorQuery.value || (book.author || '').toLowerCase().includes(authorQuery.value.toLowerCase());
        const genreMatch = selectedGenres.value.length === 0 || selectedGenres.value.includes(book.genre);
        const themeMatch = selectedThemes.value.length === 0 || selectedThemes.value.includes(book.theme);
        const tagMatch = selectedTags.value.length === 0 || (book.tags || []).some((tag) => selectedTags.value.includes(tag));
        return authorMatch && genreMatch && themeMatch && tagMatch;
      });
    });

    watch(search, (value) => {
      bookStore.setSearchQuery(value);
    });

    const addGenre = (value) => {
      if (value && value.trim()) {
        bookStore.addCustomGenre(value.trim());
      }
    };

    const addTheme = (value) => {
      if (value && value.trim()) {
        bookStore.addCustomTheme(value.trim());
      }
    };

    const addTag = (value) => {
      if (value && value.trim()) {
        const next = value.trim();
        if (!selectedTags.value.includes(next)) {
          selectedTags.value = [...new Set([...selectedTags.value, next])];
        }
      }
    };

    const removeGenre = (value) => {
      bookStore.removeCustomGenre(value);
    };

    const removeTheme = (value) => {
      bookStore.removeCustomTheme(value);
    };

    const removeTag = (value) => {
      bookStore.removeTag(value);
    };

    const clearFilters = () => {
      authorQuery.value = '';
      selectedGenres.value = [];
      selectedThemes.value = [];
      selectedTags.value = [];
      search.value = '';
      bookStore.clearAllFilters();
    };

    const openAddDialog = () => {
      editingBook.value = null;
      addMode.value = 'add';
      showAddBookModal.value = true;
    };

    const openEdit = (book) => {
      editingBook.value = book;
      addMode.value = 'edit';
      showAddBookModal.value = true;
    };

    const openDetail = (book) => {
      selectedBook.value = book;
    };

    const confirmDelete = (book) => {
      if (confirm(`确定删除《${book.title}》吗？`)) {
        bookStore.deleteBook(book.id);
        if (selectedBook.value?.id === book.id) selectedBook.value = null;
      }
    };

    const closeDialog = () => {
      showAddBookModal.value = false;
      editingBook.value = null;
      addMode.value = 'add';
    };

    const closeBookDetailModal = () => {
      selectedBook.value = null;
    };

    const openJournal = () => {
      if (!selectedBook.value) return;
      router.push({ path: '/editor', query: { bookId: selectedBook.value.id } });
    };

    const handleImageError = (event) => {
      event.target.src = 'https://via.placeholder.com/300x450?text=No+Cover';
    };

    const visibleBooks = filteredBooks;
    const totalBooks = computed(() => filteredBooks.value.length);
    const hasAnyFilter = computed(() => {
      return (
        authorQuery.value ||
        selectedGenres.value.length > 0 ||
        selectedThemes.value.length > 0 ||
        selectedTags.value.length > 0
      );
    });

    return {
      bookStore,
      allGenres,
      allThemes,
      allTags,
      search,
      authorQuery,
      selectedGenres,
      selectedThemes,
      selectedTags,
      addGenre,
      addTheme,
      addTag,
      removeGenre,
      removeTheme,
      removeTag,
      clearFilters,
      filteredBooks,
      totalBooks,
      showAddBookModal,
      selectedBook,
      editingBook,
      addMode,
      openAddDialog,
      openEdit,
      openDetail,
      confirmDelete,
      closeDialog,
      closeBookDetailModal,
      openJournal,
      handleImageError,
      hasAnyFilter,
    };
  },
};
</script>

<style scoped>
.bookshelf-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f4e4bc 0%, #f9f6f0 50%, #e8dcc0 100%);
  font-family: 'Georgia', serif;
  padding: 30px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 36px;
  margin: 0 0 10px 0;
  border-bottom: 3px solid #d4af37;
  padding-bottom: 15px;
  display: inline-block;
}

.page-header p {
  color: #8b7355;
  font-size: 18px;
  margin: 0;
  font-style: italic;
}

.toolbar {
  margin: 14px auto 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: center;
}
.search-input {
  width: min(400px, 100%);
  border: 1px solid #d4af37;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #4b3928;
}
.clear-filters-btn {
  border: none;
  background: #8b7355;
  color: #fff;
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
}
.content-layout {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.filter-sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.bookshelf-main {
  min-height: 600px;
}

.bookshelf-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 25px;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
}

.header-info h2 {
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 28px;
  margin: 0 0 10px 0;
}

.filtered-text {
  color: #8b7355;
  font-size: 16px;
  font-weight: normal;
  font-style: italic;
}

.add-book-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  border: 2px solid #b8860b;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
}

.add-book-btn:hover {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.filter-section {
      margin-bottom: 16px;
      border: 1px solid #e8dcc0;
      background: #fffdf6;
      border-radius: 10px;
      padding: 10px;
    }

    .filter-header {
      font-weight: bold;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #5d4e37;
      margin-bottom: 8px;
    }

    .filter-options {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: 6px;
      font-size: 14px;
      color: #5d4e37;
    }

    .filter-options label {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .filter-input {
      width: 100%;
      border: 1px solid #d4af37;
      border-radius: 6px;
      padding: 6px 10px;
      background: #fff;
      margin-bottom: 6px;
    }

    .add-row {
      display: flex;
      gap: 6px;
      margin-bottom: 8px;
    }

    .tag-add {
      border: 1px solid #d4af37;
      background: #f6e9c7;
      color: #5d4e37;
      border-radius: 6px;
      padding: 6px 10px;
      cursor: pointer;
    }

    .empty-bookshelf {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 400px;
    }

    .empty-content {
  text-align: center;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  padding: 50px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  max-width: 600px;
}

.empty-content h3 {
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 28px;
  margin: 0 0 15px 0;
}

.empty-content p {
  color: #8b7355;
  font-size: 16px;
  margin: 0 0 30px 0;
  line-height: 1.5;
}

.empty-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.clear-filters-btn,
.add-first-book-btn {
  padding: 12px 24px;
  border: 2px solid;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
}

.clear-filters-btn {
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  color: #f9f6f0;
  border-color: #a0865c;
}

.clear-filters-btn:hover {
  background: linear-gradient(135deg, #a0865c 0%, #b8976a 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(139, 115, 85, 0.3);
}

.add-first-book-btn {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  border-color: #b8860b;
}

.add-first-book-btn:hover {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(212, 175, 55, 0.3);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(93, 78, 55, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow:
    0 8px 30px rgba(139, 115, 85, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 2px solid #e8dcc0;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 2px solid #e8dcc0;
}

.modal-header h2 {
  margin: 0;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 28px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  color: #8b7355;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(139, 115, 85, 0.1);
}

/* Add Book Form Styles */
.add-book-form {
  padding: 30px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #5d4e37;
  font-weight: bold;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #e8dcc0;
  border-radius: 6px;
  font-size: 16px;
  background: #fefcf8;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-help {
  display: block;
  margin-top: 5px;
  color: #8b7355;
  font-size: 12px;
  font-style: italic;
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding: 25px 30px;
  border-top: 2px solid #e8dcc0;
  background: linear-gradient(135deg, #f9f6f0 0%, #f4e4bc 100%);
}

.save-btn,
.cancel-btn,
.journal-btn,
.delete-btn,
.close-modal-btn {
  padding: 12px 24px;
  border: 2px solid;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
}

.save-btn {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  border-color: #b8860b;
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

.cancel-btn,
.close-modal-btn {
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  color: #f9f6f0;
  border-color: #a0865c;
}

.cancel-btn:hover,
.close-modal-btn:hover {
  background: linear-gradient(135deg, #a0865c 0%, #b8976a 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(139, 115, 85, 0.3);
}

.journal-btn {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  border-color: #b8860b;
}

.journal-btn:hover {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(212, 175, 55, 0.3);
}

.delete-btn {
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  color: #f9f6f0;
  border-color: #a0865c;
}

.delete-btn:hover {
  background: linear-gradient(135deg, #a0865c 0%, #b8976a 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(139, 115, 85, 0.3);
}

/* Book Detail Modal Content */
.modal-content {
  padding: 30px;
}

.book-detail-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 30px;
}

.book-cover-large {
  text-align: center;
}

.book-cover-large img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow:
    0 6px 20px rgba(0, 0, 0, 0.2),
    0 0 0 2px rgba(139, 115, 85, 0.1);
  border: 2px solid #e8dcc0;
}

.book-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-section h3 {
  margin: 0 0 8px 0;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 18px;
  border-bottom: 1px solid #d4af37;
  padding-bottom: 4px;
}

.detail-section p {
  margin: 0;
  color: #5d4e37;
  line-height: 1.5;
  font-size: 16px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tags-list .tag {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .content-layout {
    grid-template-columns: 320px 1fr;
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .bookshelf-page {
    padding: 20px;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .content-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .bookshelf-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .book-detail-layout {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .book-cover-large {
    order: -1;
  }

  .modal {
    width: 95%;
    margin: 20px;
  }

  .modal-header,
  .modal-content,
  .add-book-form,
  .modal-actions {
    padding-left: 20px;
    padding-right: 20px;
  }

  .empty-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>
