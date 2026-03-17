<template>
  <div class="book-filter-page">
    <div class="page-header">
      <h1>书籍筛选</h1>
      <p>通过多维筛选管理您的阅读书库</p>
    </div>

    <div class="content-layout">
      <aside class="filter-sidebar">
        <FilterPanel />
      </aside>

      <main class="books-main">
        <div class="books-header">
          <h2>
            {{ filteredBooks.length }} 本书
            <span v-if="hasActiveFilters" class="filtered-text">
              （从 {{ books.length }} 本中筛选）
            </span>
          </h2>
        </div>

        <div class="books-grid" v-if="filteredBooks.length > 0">
          <BookCard
            v-for="book in filteredBooks"
            :key="book.id"
            :book="book"
            @click="handleBookClick"
          />
        </div>

        <div v-else class="no-books">
          <div class="no-books-content">
            <h3>没有书籍符合当前筛选条件</h3>
            <p>
              尝试调整筛选条件，或清除筛选以查看所有书籍。
            </p>
            <button @click="clearAllFilters" class="clear-filters-btn">
              清除所有筛选
            </button>
          </div>
        </div>
      </main>
    </div>

    <!-- Book Detail Modal -->
    <div v-if="selectedBook" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedBook.title }}</h2>
          <button @click="closeModal" class="close-btn">&times;</button>
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
          <button @click="openJournal" class="journal-btn">
            打开手账
          </button>
          <button @click="closeModal" class="close-modal-btn">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useBookStore } from '../stores/books.js';
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue';
import BookCard from './BookCard.vue';
import FilterPanel from './FilterPanel.vue';

export default {
  name: 'BookFilter',
  components: {
    BookCard,
    FilterPanel,
  },
  setup() {
    const bookStore = useBookStore();
    const router = useRouter();
    const selectedBook = ref(null);

    const books = computed(() => bookStore.books);
    const filteredBooks = computed(() => bookStore.filteredBooks);

    const hasActiveFilters = computed(() => {
      return (
        bookStore.selectedCategory.length > 0 ||
        bookStore.selectedAuthor.length > 0 ||
        bookStore.selectedTags.length > 0
      );
    });

    const handleBookClick = (book) => {
      selectedBook.value = book;
    };

    const closeModal = () => {
      selectedBook.value = null;
    };

    const openJournal = () => {
      if (selectedBook.value) {
        router.push({
          path: '/editor',
          query: { bookId: selectedBook.value.id },
        });
      }
    };

    const clearAllFilters = () => {
      bookStore.clearAllFilters();
    };

    const handleImageError = (event) => {
      event.target.src = 'https://via.placeholder.com/300x450?text=No+Cover';
    };

    return {
      books,
      filteredBooks,
      selectedBook,
      hasActiveFilters,
      handleBookClick,
      closeModal,
      openJournal,
      clearAllFilters,
      handleImageError,
    };
  },
};
</script>

<style scoped>
.book-filter-page {
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

.books-main {
  min-height: 600px;
}

.books-header {
  margin-bottom: 30px;
}

.books-header h2 {
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

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.no-books {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.no-books-content {
  text-align: center;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  padding: 40px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  max-width: 500px;
}

.no-books-content h3 {
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 24px;
  margin: 0 0 15px 0;
}

.no-books-content p {
  color: #8b7355;
  font-size: 16px;
  margin: 0 0 25px 0;
  line-height: 1.5;
}

.clear-filters-btn {
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

.clear-filters-btn:hover {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
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
  max-width: 800px;
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

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding: 25px 30px;
  border-top: 2px solid #e8dcc0;
  background: linear-gradient(135deg, #f9f6f0 0%, #f4e4bc 100%);
}

.journal-btn,
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

.close-modal-btn {
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  color: #f9f6f0;
  border-color: #a0865c;
}

.close-modal-btn:hover {
  background: linear-gradient(135deg, #a0865c 0%, #b8976a 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(139, 115, 85, 0.3);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .content-layout {
    grid-template-columns: 320px 1fr;
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .book-filter-page {
    padding: 20px;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .content-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
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
  .modal-actions {
    padding-left: 20px;
    padding-right: 20px;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
