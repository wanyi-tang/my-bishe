import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import bookApi from '../services/bookService';

export const useBookStore = defineStore('books', () => {
  const books = ref([]);
  const loading = ref(false);
  const error = ref(null);

  // Filter state
  const searchQuery = ref('');
  const selectedGenres = ref([]);
  const selectedThemes = ref([]);
  const selectedTags = ref([]);

  const defaultGenres = ref(['诗歌', '小说', '散文', '戏剧']);
  const defaultThemes = ref(['历史', '现实', '农村', '都市', '军旅', '爱情', '悬疑', '科幻', '玄幻', '儿童', '武侠']);

  // Fetch books from API
  const fetchBooks = async (params = {}) => {
    loading.value = true;
    error.value = null;
    try {
      const data = await bookApi.getAllBooks(params);
      books.value = data;
      return data;
    } catch (err) {
      error.value = err.message;
      console.error('Failed to fetch books:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const addBook = async (bookData) => {
    loading.value = true;
    error.value = null;
    try {
      const newBook = await bookApi.createBook(bookData);
      books.value.push(newBook);
      return newBook;
    } catch (err) {
      error.value = err.message;
      console.error('Failed to add book:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateBook = async (id, updatedBook) => {
    loading.value = true;
    error.value = null;
    try {
      const book = await bookApi.updateBook(id, updatedBook);
      const index = books.value.findIndex(b => b._id === id || b.id === id);
      if (index !== -1) {
        books.value[index] = book;
      }
      return book;
    } catch (err) {
      error.value = err.message;
      console.error('Failed to update book:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteBook = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      await bookApi.deleteBook(id);
      books.value = books.value.filter(b => b._id !== id && b.id !== id);
    } catch (err) {
      error.value = err.message;
      console.error('Failed to delete book:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getBookById = (id) => {
    return books.value.find(b => b._id === id || b.id === id);
  };

  // Filter-related computed properties
  const allGenres = computed(() => {
    const genres = new Set(defaultGenres.value);
    books.value.forEach(book => { if (book.genre) genres.add(book.genre); });
    return Array.from(genres).sort();
  });

  const allThemes = computed(() => {
    const themes = new Set(defaultThemes.value);
    books.value.forEach(book => { if (book.theme) themes.add(book.theme); });
    return Array.from(themes).sort();
  });

  const allTags = computed(() => {
    const tags = new Set();
    books.value.forEach(book => {
      if (book.tags && Array.isArray(book.tags)) {
        book.tags.forEach(tag => tags.add(tag));
      }
    });
    return Array.from(tags).sort();
  });

  const filteredBooks = computed(() => {
    const q = searchQuery.value.trim().toLowerCase();
    return books.value.filter(book => {
      if (q && !book.title.toLowerCase().includes(q)) {
        return false;
      }
      if (selectedGenres.value.length > 0 && !selectedGenres.value.includes(book.genre)) {
        return false;
      }
      if (selectedThemes.value.length > 0 && !selectedThemes.value.includes(book.theme)) {
        return false;
      }
      if (selectedTags.value.length > 0) {
        if (!book.tags || !Array.isArray(book.tags)) return false;
        const hasAllTags = selectedTags.value.every(tag => book.tags.includes(tag));
        if (!hasAllTags) return false;
      }
      return true;
    });
  });

  // Filter management methods
  const setSearchQuery = (value) => {
    searchQuery.value = value;
  };

  const updateSelectedGenres = (genres) => {
    selectedGenres.value = genres;
  };

  const updateSelectedThemes = (themes) => {
    selectedThemes.value = themes;
  };

  const updateSelectedTags = (tags) => {
    selectedTags.value = tags;
  };

  const addCustomGenre = (genre) => {
    const cleaned = genre?.trim();
    if (cleaned && !defaultGenres.value.includes(cleaned)) {
      defaultGenres.value.push(cleaned);
    }
  };

  const addCustomTheme = (theme) => {
    const cleaned = theme?.trim();
    if (cleaned && !defaultThemes.value.includes(cleaned)) {
      defaultThemes.value.push(cleaned);
    }
  };

  const removeCustomGenre = (genre) => {
    defaultGenres.value = defaultGenres.value.filter((g) => g !== genre);
    selectedGenres.value = selectedGenres.value.filter((g) => g !== genre);
  };

  const removeCustomTheme = (theme) => {
    defaultThemes.value = defaultThemes.value.filter((t) => t !== theme);
    selectedThemes.value = selectedThemes.value.filter((t) => t !== theme);
  };

  const removeTag = (tag) => {
    selectedTags.value = selectedTags.value.filter((t) => t !== tag);
    books.value = books.value.map((book) => {
      if (book.tags && Array.isArray(book.tags) && book.tags.includes(tag)) {
        return { ...book, tags: book.tags.filter((t) => t !== tag) };
      }
      return book;
    });
  };

  const clearAllFilters = () => {
    searchQuery.value = '';
    selectedGenres.value = [];
    selectedThemes.value = [];
    selectedTags.value = [];
  };

  return {
    books,
    loading,
    error,
    searchQuery,
    selectedGenres,
    selectedThemes,
    selectedTags,
    allGenres,
    allThemes,
    allTags,
    filteredBooks,
    fetchBooks,
    addBook,
    updateBook,
    deleteBook,
    getBookById,
    setSearchQuery,
    updateSelectedGenres,
    updateSelectedThemes,
    updateSelectedTags,
    addCustomGenre,
    addCustomTheme,
    removeCustomGenre,
    removeCustomTheme,
    removeTag,
    clearAllFilters,
  };
});
