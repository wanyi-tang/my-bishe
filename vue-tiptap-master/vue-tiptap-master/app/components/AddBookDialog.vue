<template>
  <div v-if="show" class="dialog-mask" @click.self="close">
    <div class="dialog-card">
      <div class="dialog-header">
        <h3>{{ mode === 'edit' ? '编辑书籍' : '添加书籍' }}</h3>
        <button @click="close">✕</button>
      </div>
      <form @submit.prevent="saveBook" class="dialog-form">
        <div class="field-group">
          <label>书名 *</label>
          <input v-model="form.title" required />
        </div>
        <div class="field-group">
          <label>作者 *</label>
          <input v-model="form.author" required />
        </div>
        <div class="field-group">
          <label>文学体裁 *</label>
          <div class="select-with-add">
            <select v-model="form.genre" required>
              <option value="">请选择</option>
              <option v-for="genre in allGenres" :key="genre" :value="genre">{{ genre }}</option>
            </select>
            <button type="button" @click="addNewGenre" class="add-button">+</button>
          </div>
        </div>
        <div class="field-group">
          <label>文学题材 *</label>
          <div class="select-with-add">
            <select v-model="form.theme" required>
              <option value="">请选择</option>
              <option v-for="theme in allThemes" :key="theme" :value="theme">{{ theme }}</option>
            </select>
            <button type="button" @click="addNewTheme" class="add-button">+</button>
          </div>
        </div>
        <div class="field-group">
          <label>标签 (逗号分隔)</label>
          <div class="input-with-add">
            <input v-model="tagsText" placeholder="例如：经典,心灵" />
            <button type="button" @click="addNewTag" class="add-button">+</button>
          </div>
        </div>
        <div class="field-group">
          <label>封面地址</label>
          <input v-model="form.cover" placeholder="https://..." />
        </div>
        <div class="field-group">
          <label>描述</label>
          <textarea v-model="form.description" rows="3"></textarea>
        </div>
        <div class="dialog-actions">
          <button type="submit" :disabled="!isValid">保存</button>
          <button type="button" class="cancel" @click="close">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useBookStore } from '../stores/books.js';

const props = defineProps({
  show: Boolean,
  mode: { type: String, default: 'add' },
  book: { type: Object, default: null },
});
const emit = defineEmits(['close', 'saved']);

const store = useBookStore();
const form = ref({
  id: null,
  title: '',
  author: '',
  genre: '',
  theme: '',
  cover: '',
  description: '',
  tags: [],
});
const tagsText = ref('');

const reset = () => {
  form.value = {
    id: null,
    title: '',
    author: '',
    genre: '',
    theme: '',
    cover: '',
    description: '',
    tags: [],
  };
  tagsText.value = '';
};

watch(() => props.book, (book) => {
  if (book) {
    form.value = { ...book, tags: book.tags || [] };
    tagsText.value = (book.tags || []).join(',');
  } else {
    reset();
  }
}, { immediate: true });

const allGenres = computed(() => store.allGenres);
const allThemes = computed(() => store.allThemes);
const isValid = computed(() => {
  return form.value.title.trim() && form.value.author.trim() && form.value.genre && form.value.theme;
});

const saveBook = () => {
  form.value.tags = tagsText.value
    .split(',')
    .map((t) => t.trim())
    .filter((t) => t);
  const bookData = { ...form.value };
  if (props.mode === 'edit' && bookData.id) {
    store.updateBook(bookData.id, bookData);
  } else {
    store.addBook(bookData);
  }
  emit('saved');
  close();
};

const close = () => {
  emit('close');
  reset();
};

const addNewGenre = () => {
  const newGenre = prompt('请输入新的文学体裁：');
  if (newGenre && newGenre.trim()) {
    store.addCustomGenre(newGenre.trim());
  }
};

const addNewTheme = () => {
  const newTheme = prompt('请输入新的文学题材：');
  if (newTheme && newTheme.trim()) {
    store.addCustomTheme(newTheme.trim());
  }
};

const addNewTag = () => {
  const newTag = prompt('请输入新的标签：');
  if (newTag && newTag.trim()) {
    const currentTags = tagsText.value ? tagsText.value.split(',').map(t => t.trim()).filter(t => t) : [];
    currentTags.push(newTag.trim());
    tagsText.value = currentTags.join(', ');
  }
};
</script>

<style scoped>
.dialog-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.dialog-card {
  width: min(760px, 95%);
  background: #fffdf6;
  border-radius: 12px;
  border: 1px solid #e8dcc0;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}
.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f7f1e6;
  padding: 12px 16px;
  border-bottom: 1px solid #e8dcc0;
}
.dialog-header h3 { margin: 0; color: #5d4e37; font-family: 'Georgia', serif; }
.dialog-header button { border: 0; background: none; font-size: 18px; cursor: pointer; color: #5d4e37; }
.dialog-form { padding: 16px; display: grid; gap: 12px; }
.field-group { display: grid; gap: 4px; }
.field-group label { color: #5d4e37; font-weight: 600; font-size: 13px; }
.field-group input, .field-group select, .field-group textarea {
  padding: 8px 10px;
  border: 1px solid #e8dcc0;
  border-radius: 6px;
  font-size: 14px;
  background: #fff;
}
.select-with-add, .input-with-add {
  display: flex;
  gap: 8px;
  align-items: center;
}
.add-button {
  padding: 8px 12px;
  border: 1px solid #e8dcc0;
  border-radius: 6px;
  background: #f7f1e6;
  color: #5d4e37;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}
.add-button:hover {
  background: #e8dcc0;
}
.dialog-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 4px; }
.dialog-actions button { border: 0; border-radius: 6px; padding: 8px 14px; cursor: pointer; }
.dialog-actions button:hover { filter: brightness(0.95); }
.dialog-actions button:disabled { background: #ddd; cursor: not-allowed; }
.dialog-actions button.cancel { background: #ddd; color: #5d4e37; }
.dialog-actions button:not(.cancel) { background: #d4af37; color: #fff; }
</style>