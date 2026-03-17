<template>
  <div class="filter-panel">
    <div class="filter-header">
      <h3>筛选书籍</h3>
      <button
        @click="clearAllFilters"
        class="clear-btn"
        :disabled="!hasActiveFilters"
      >
        清除全部
      </button>
    </div>

    <div class="filter-section">
      <h4>文学题材</h4>
      <div class="checkbox-group">
        <label
          v-for="category in allCategories"
          :key="category"
          class="checkbox-label"
        >
          <input
            type="checkbox"
            :value="category"
            v-model="localSelectedCategory"
            @change="updateCategories"
          />
          <span class="checkmark"></span>
          {{ category }}
        </label>
      </div>
    </div>

    <div class="filter-section">
      <h4>作者</h4>
      <div class="checkbox-group">
        <label
          v-for="author in allAuthors"
          :key="author"
          class="checkbox-label"
        >
          <input
            type="checkbox"
            :value="author"
            v-model="localSelectedAuthor"
            @change="updateAuthors"
          />
          <span class="checkmark"></span>
          {{ author }}
        </label>
      </div>
    </div>

    <div class="filter-section">
      <h4>标签</h4>
      <div class="checkbox-group">
        <label v-for="tag in allTags" :key="tag" class="checkbox-label">
          <input
            type="checkbox"
            :value="tag"
            v-model="localSelectedTags"
            @change="updateTags"
          />
          <span class="checkmark"></span>
          {{ tag }}
        </label>
      </div>
    </div>

    <div class="filter-summary" v-if="hasActiveFilters">
      <p>显示 {{ filteredBooksCount }} 本，共 {{ totalBooksCount }} 本书籍</p>
    </div>
  </div>
</template>

<script>
import { useBookStore } from '../stores/books.js';
import { computed, ref, watch } from 'vue';

export default {
  name: 'FilterPanel',
  setup() {
    const bookStore = useBookStore();

    // Local reactive copies for immediate UI updates
    const localSelectedCategory = ref([...bookStore.selectedCategory]);
    const localSelectedAuthor = ref([...bookStore.selectedAuthor]);
    const localSelectedTags = ref([...bookStore.selectedTags]);

    // Watch for external changes to sync local state
    watch(
      () => bookStore.selectedCategory,
      (newVal) => {
        localSelectedCategory.value = [...newVal];
      },
    );

    watch(
      () => bookStore.selectedAuthor,
      (newVal) => {
        localSelectedAuthor.value = [...newVal];
      },
    );

    watch(
      () => bookStore.selectedTags,
      (newVal) => {
        localSelectedTags.value = [...newVal];
      },
    );

    const allCategories = computed(() => bookStore.allCategories);
    const allAuthors = computed(() => bookStore.allAuthors);
    const allTags = computed(() => bookStore.allTags);

    const filteredBooksCount = computed(() => bookStore.filteredBooks.length);
    const totalBooksCount = computed(() => bookStore.books.length);

    const hasActiveFilters = computed(() => {
      return (
        localSelectedCategory.value.length > 0 ||
        localSelectedAuthor.value.length > 0 ||
        localSelectedTags.value.length > 0
      );
    });

    const updateCategories = () => {
      bookStore.updateSelectedCategory([...localSelectedCategory.value]);
    };

    const updateAuthors = () => {
      bookStore.updateSelectedAuthor([...localSelectedAuthor.value]);
    };

    const updateTags = () => {
      bookStore.updateSelectedTags([...localSelectedTags.value]);
    };

    const clearAllFilters = () => {
      localSelectedCategory.value = [];
      localSelectedAuthor.value = [];
      localSelectedTags.value = [];
      bookStore.clearAllFilters();
    };

    return {
      localSelectedCategory,
      localSelectedAuthor,
      localSelectedTags,
      allCategories,
      allAuthors,
      allTags,
      filteredBooksCount,
      totalBooksCount,
      hasActiveFilters,
      updateCategories,
      updateAuthors,
      updateTags,
      clearAllFilters,
    };
  },
};
</script>

<style scoped>
.filter-panel {
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  padding: 25px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  max-width: 350px;
  position: sticky;
  top: 20px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #d4af37;
}

.filter-header h3 {
  margin: 0;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 22px;
}

.clear-btn {
  padding: 8px 16px;
  background: linear-gradient(135deg, #8b7355 0%, #a0865c 100%);
  color: #f9f6f0;
  border: 2px solid #a0865c;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  font-family: 'Georgia', serif;
  transition: all 0.3s ease;
}

.clear-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #a0865c 0%, #b8976a 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(139, 115, 85, 0.3);
}

.clear-btn:disabled {
  background: #e8dcc0;
  border-color: #d4af37;
  color: #8b7355;
  cursor: not-allowed;
  transform: none;
}

.filter-section {
  margin-bottom: 30px;
}

.filter-section h4 {
  margin: 0 0 15px 0;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #e8dcc0;
  padding-bottom: 5px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 14px;
  color: #5d4e37;
}

.checkbox-label:hover {
  background: rgba(212, 175, 55, 0.1);
}

.checkbox-label input[type='checkbox'] {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  position: relative;
  height: 18px;
  width: 18px;
  background-color: #fefcf8;
  border: 2px solid #e8dcc0;
  border-radius: 3px;
  margin-right: 12px;
  transition: all 0.2s ease;
}

.checkbox-label input[type='checkbox']:checked ~ .checkmark {
  background-color: #d4af37;
  border-color: #b8860b;
}

.checkmark:after {
  content: '';
  position: absolute;
  display: none;
}

.checkbox-label input[type='checkbox']:checked ~ .checkmark:after {
  display: block;
}

.checkbox-label .checkmark:after {
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.filter-summary {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e8dcc0;
  text-align: center;
}

.filter-summary p {
  margin: 0;
  color: #8b7355;
  font-style: italic;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .filter-panel {
    max-width: 300px;
  }
}

@media (max-width: 768px) {
  .filter-panel {
    position: static;
    max-width: 100%;
    margin-bottom: 30px;
  }

  .filter-header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
