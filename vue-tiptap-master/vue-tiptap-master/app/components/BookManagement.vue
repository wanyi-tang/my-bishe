<template>
  <div class="book-management">
    <div class="header">
      <h2>书籍管理</h2>
      <button @click="openModal()" class="add-btn">添加书籍</button>
    </div>

    <div class="books-grid">
      <div v-for="book in books" :key="book.id" class="book-card">
        <div class="book-cover">
          <img
            :src="
              book.cover || 'https://via.placeholder.com/150x200?text=No+Cover'
            "
            :alt="book.title"
          />
        </div>
        <div class="book-info">
          <h3>{{ book.title }}</h3>
          <p class="author">作者：{{ book.author }}</p>
          <p class="genre">{{ book.genre }}</p>
        </div>
        <div class="book-actions">
          <button @click="openModal(book)" class="edit-btn">编辑</button>
          <button @click="deleteBook(book.id)" class="delete-btn">
            删除
          </button>
        </div>
      </div>
    </div>

    <!-- Modal for Add/Edit -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h3>{{ isEditing ? '编辑书籍' : '添加新书' }}</h3>
        <form @submit.prevent="saveBook">
          <div class="form-group">
            <label for="title">书名：</label>
            <input id="title" v-model="formData.title" required />
          </div>
          <div class="form-group">
            <label for="author">作者：</label>
            <input id="author" v-model="formData.author" required />
          </div>
          <div class="form-group">
            <label for="genre">文学题材：</label>
            <input id="genre" v-model="formData.genre" />
          </div>
          <div class="form-group">
            <label for="cover">封面地址：</label>
            <input
              id="cover"
              v-model="formData.cover"
              placeholder="https://..."
            />
          </div>
          <div class="modal-actions">
            <button type="submit" class="save-btn">
              {{ isEditing ? '更新' : '添加' }}
            </button>
            <button type="button" @click="closeModal" class="cancel-btn">
              取消
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useBookStore } from '../stores/books.js';
import { ref, computed } from 'vue';

export default {
  name: 'BookManagement',
  setup() {
    const bookStore = useBookStore();
    const showModal = ref(false);
    const isEditing = ref(false);
    const formData = ref({
      id: null,
      title: '',
      author: '',
      genre: '',
      cover: '',
    });

    const openModal = (book = null) => {
      if (book) {
        isEditing.value = true;
        formData.value = { ...book };
      } else {
        isEditing.value = false;
        formData.value = {
          id: null,
          title: '',
          author: '',
          genre: '',
          cover: '',
        };
      }
      showModal.value = true;
    };

    const closeModal = () => {
      showModal.value = false;
      formData.value = {
        id: null,
        title: '',
        author: '',
        genre: '',
        cover: '',
      };
    };

    const saveBook = () => {
      if (isEditing.value) {
        bookStore.updateBook(formData.value.id, formData.value);
      } else {
        bookStore.addBook(formData.value);
      }
      closeModal();
    };

    const deleteBook = (id) => {
      if (confirm('确定要删除这本书吗？')) {
        bookStore.deleteBook(id);
      }
    };

    return {
      books: computed(() => bookStore.books),
      showModal,
      isEditing,
      formData,
      openModal,
      closeModal,
      saveBook,
      deleteBook,
    };
  },
};
</script>

<style scoped>
.book-management {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
  background: linear-gradient(135deg, #f4e4bc 0%, #f9f6f0 50%, #e8dcc0 100%);
  min-height: 100vh;
  font-family: 'Georgia', serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding: 25px;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
}

.header h2 {
  margin: 0;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 28px;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 8px;
}

.add-btn {
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

.add-btn:hover {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.book-card {
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-8px);
  box-shadow:
    0 8px 25px rgba(139, 115, 85, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.book-cover {
  height: 220px;
  overflow: hidden;
  position: relative;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.book-card:hover .book-cover img {
  transform: scale(1.05);
}

.book-info {
  padding: 20px;
}

.book-info h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: #5d4e37;
  line-height: 1.3;
  font-weight: bold;
}

.author {
  margin: 0 0 8px 0;
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

.book-actions {
  padding: 20px;
  display: flex;
  gap: 12px;
  background: linear-gradient(135deg, #f9f6f0 0%, #f4e4bc 100%);
}

.edit-btn,
.delete-btn {
  flex: 1;
  padding: 10px 16px;
  border: 2px solid;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
}

.edit-btn {
  background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
  color: #5d4e37;
  border-color: #b8860b;
}

.edit-btn:hover {
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
  padding: 35px;
  border-radius: 12px;
  width: 90%;
  max-width: 550px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow:
    0 8px 30px rgba(139, 115, 85, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 2px solid #e8dcc0;
}

.modal h3 {
  margin-top: 0;
  margin-bottom: 25px;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 24px;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 8px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #5d4e37;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #e8dcc0;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box;
  background: #fefcf8;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}

.modal-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.save-btn,
.cancel-btn {
  flex: 1;
  padding: 12px 20px;
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

.save-btn:hover {
  background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(212, 175, 55, 0.3);
}

.cancel-btn {
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  color: #f9f6f0;
  border-color: #a0865c;
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #a0865c 0%, #b8976a 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(139, 115, 85, 0.3);
}

/* Responsive Design */
@media (max-width: 768px) {
  .book-management {
    padding: 20px;
  }

  .header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }

  .book-actions {
    flex-direction: column;
  }

  .modal {
    width: 95%;
    padding: 25px;
  }
}
</style>
