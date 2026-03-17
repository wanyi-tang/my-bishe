<template>
  <div class="book-filter-panel">
    <div class="panel-title-row">
      <h3>筛选</h3>
      <button class="clear-all" @click="clearAll">清除筛选</button>
    </div>

    <div class="filter-section">
      <div class="filter-header" @click="showGenre = !showGenre">
        <span>文学体裁</span>
        <span>{{ showGenre ? '▼' : '▶' }}</span>
      </div>
      <div v-if="showGenre" class="filter-body">
        <div class="option-row" v-for="genre in genres" :key="genre"
          @mousedown="startLongPress(() => confirmDelete('genre', genre))"
          @mouseup="cancelLongPress"
          @mouseleave="cancelLongPress"
          @touchstart.prevent="startLongPress(() => confirmDelete('genre', genre))"
          @touchend.prevent="cancelLongPress"
        >
          <label>
            <input
              type="checkbox"
              :value="genre"
              v-model="localSelectedGenres"
            />
            {{ genre }}
          </label>
        </div>
        <div class="add-row">
          <button class="add-btn" @click="showAddGenre = true">+ 添加</button>
          <div v-if="showAddGenre" class="add-inline">
            <input v-model="genreInput" @keyup.enter="submitGenre" placeholder="新体裁" />
            <button @click="submitGenre">确定</button>
          </div>
        </div>
      </div>
    </div>

    <div class="filter-section">
      <div class="filter-header" @click="showTheme = !showTheme">
        <span>文学题材</span>
        <span>{{ showTheme ? '▼' : '▶' }}</span>
      </div>
      <div v-if="showTheme" class="filter-body">
        <div class="option-row" v-for="theme in themes" :key="theme"
          @mousedown="startLongPress(() => confirmDelete('theme', theme))"
          @mouseup="cancelLongPress"
          @mouseleave="cancelLongPress"
          @touchstart.prevent="startLongPress(() => confirmDelete('theme', theme))"
          @touchend.prevent="cancelLongPress"
        >
          <label>
            <input
              type="checkbox"
              :value="theme"
              v-model="localSelectedThemes"
            />
            {{ theme }}
          </label>
        </div>
        <div class="add-row">
          <button class="add-btn" @click="showAddTheme = true">+ 添加</button>
          <div v-if="showAddTheme" class="add-inline">
            <input v-model="themeInput" @keyup.enter="submitTheme" placeholder="新题材" />
            <button @click="submitTheme">确定</button>
          </div>
        </div>
      </div>
    </div>

    <div class="filter-section">
      <div class="filter-header" @click="showTags = !showTags">
        <span>标签</span>
        <span>{{ showTags ? '▼' : '▶' }}</span>
      </div>
      <div v-if="showTags" class="filter-body">
        <div class="option-row" v-for="tag in tags" :key="tag"
          @mousedown="startLongPress(() => confirmDelete('tag', tag))"
          @mouseup="cancelLongPress"
          @mouseleave="cancelLongPress"
          @touchstart.prevent="startLongPress(() => confirmDelete('tag', tag))"
          @touchend.prevent="cancelLongPress"
        >
          <label>
            <input
              type="checkbox"
              :value="tag"
              v-model="localSelectedTags"
            />
            {{ tag }}
          </label>
        </div>
        <div class="add-row">
          <button class="add-btn" @click="showAddTag = true">+ 添加</button>
          <div v-if="showAddTag" class="add-inline">
            <input v-model="tagInput" @keyup.enter="submitTag" placeholder="新标签" />
            <button @click="submitTag">确定</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
const props = defineProps({
  genres: { type: Array, required: true },
  themes: { type: Array, required: true },
  tags: { type: Array, required: true },
  selectedGenres: { type: Array, required: true },
  selectedThemes: { type: Array, required: true },
  selectedTags: { type: Array, required: true },
});
const emit = defineEmits([
  'update:selectedGenres',
  'update:selectedThemes',
  'update:selectedTags',
  'add-genre',
  'add-theme',
  'add-tag',
  'remove-genre',
  'remove-theme',
  'remove-tag',
  'clear',
]);

const showGenre = ref(true);
const showTheme = ref(true);
const showTags = ref(true);
const showAddGenre = ref(false);
const showAddTheme = ref(false);
const showAddTag = ref(false);
const genreInput = ref('');
const themeInput = ref('');
const tagInput = ref('');

const localSelectedGenres = ref([...props.selectedGenres]);
const localSelectedThemes = ref([...props.selectedThemes]);
const localSelectedTags = ref([...props.selectedTags]);

watch(
  () => props.selectedGenres,
  (v) => {
    localSelectedGenres.value = [...v];
  }
);
watch(
  () => props.selectedThemes,
  (v) => {
    localSelectedThemes.value = [...v];
  }
);
watch(
  () => props.selectedTags,
  (v) => {
    localSelectedTags.value = [...v];
  }
);

watch(localSelectedGenres, (v) => {
  emit('update:selectedGenres', [...v]);
});
watch(localSelectedThemes, (v) => {
  emit('update:selectedThemes', [...v]);
});
watch(localSelectedTags, (v) => {
  emit('update:selectedTags', [...v]);
});

const submitGenre = () => {
  const value = genreInput.value.trim();
  if (!value) return;
  emit('add-genre', value);
  genreInput.value = '';
  showAddGenre.value = false;
};

const submitTheme = () => {
  const value = themeInput.value.trim();
  if (!value) return;
  emit('add-theme', value);
  themeInput.value = '';
  showAddTheme.value = false;
};

const submitTag = () => {
  const value = tagInput.value.trim();
  if (!value) return;
  emit('add-tag', value);
  tagInput.value = '';
  showAddTag.value = false;
};

const removeGenre = (genre) => {
  emit('remove-genre', genre);
};
const removeTheme = (theme) => {
  emit('remove-theme', theme);
};
const confirmDelete = (type, value) => {
  if (!value) return;
  const label = type === 'genre' ? '体裁' : type === 'theme' ? '题材' : '标签';
  if (window.confirm(`长按检测：确定删除 ${label} “${value}” 吗？`)) {
    if (type === 'genre') removeGenre(value);
    else if (type === 'theme') removeTheme(value);
    else if (type === 'tag') emit('remove-tag', value);
  }
};
const longPressTimer = ref(null);

const startLongPress = (callback) => {
  cancelLongPress();
  longPressTimer.value = setTimeout(() => {
    callback();
    longPressTimer.value = null;
  }, 700);
};

const cancelLongPress = () => {
  if (longPressTimer.value) {
    clearTimeout(longPressTimer.value);
    longPressTimer.value = null;
  }
};

const clearAll = () => {
  emit('clear');
};
</script>

<style scoped>
.book-filter-panel { background: #fffdf6; border: 1px solid #e8dcc0; border-radius: 14px; padding: 12px; }
.panel-title-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.panel-title-row h3 { margin: 0; color: #5d4e37; font-family: Georgia, serif; }
.clear-all { border: 1px solid #d4af37; background: #f7e7b7; color: #5d4e37; border-radius: 6px; padding: 4px 10px; cursor: pointer; font-size: 12px; }
.filter-section { border: 1px solid #e8dcc0; border-radius: 10px; margin-bottom: 10px; background: #fff; }
.filter-header { display: flex; justify-content: space-between; align-items: center; cursor: pointer; padding: 8px 10px; background: #f7f1e6; border-radius: 10px 10px 0 0; font-weight: 600; color: #5d4e37; }
.filter-body { padding: 10px; }
  .option-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; padding: 4px 0; }
.option-row label { display: flex; align-items: center; gap: 6px; font-size: 14px; color: #5d4e37; }  .long-press-tip { font-size: 12px; color: #a84545; margin-left: 10px; }.remove-option { border: none; background: transparent; color: #c94444; cursor: pointer; font-weight: bold; }
.add-row { margin-top: 8px; display: flex; align-items: center; gap: 6px; }
.add-btn { border: 1px solid #d4af37; background: #f7e8af; border-radius: 6px; color: #5d4e37; cursor: pointer; padding: 4px 8px; }
.add-inline { display: flex; align-items: center; gap: 6px; margin-top: 6px; }
.add-inline input { border: 1px solid #e8dcc0; border-radius: 6px; padding: 5px 8px; flex: 1; }
.add-inline button { border: 1px solid #d4af37; background: #f7e8af; border-radius: 6px; color: #5d4e37; cursor: pointer; padding: 4px 8px; }
</style>