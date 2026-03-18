import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useBookStore = defineStore('books', () => {
    const books = ref(JSON.parse(localStorage.getItem('books') || '[]'));

    // Filter state
    const searchQuery = ref('');
    const selectedGenres = ref([]);
    const selectedThemes = ref([]);
    const selectedTags = ref([]);

    const defaultGenres = ref(['诗歌', '小说', '散文', '戏剧']);
    const defaultThemes = ref(['历史', '现实', '农村', '都市', '军旅', '爱情', '悬疑', '科幻', '玄幻', '儿童', '武侠']);
    const customTags = ref(JSON.parse(localStorage.getItem('customTags') || '[]'));

    const saveToStorage = () => {
        localStorage.setItem('books', JSON.stringify(books.value));
        localStorage.setItem('customTags', JSON.stringify(customTags.value));
    };

    // Initialize with dummy data if no books exist
    const initializeDummyData = () => {
        if (books.value.length === 0) {
            const dummyBooks = [
                {
                    id: 1,
                    title: "三体",
                    author: "刘慈欣",
                    genre: "小说",
                    theme: "科幻",
                    cover: "https://picsum.photos/200/300?random=1",
                    tags: ["中国文学", "科幻"],
                    description: "一部关于宇宙文明的科幻巨作。"
                },
                {
                    id: 2,
                    title: "红楼梦",
                    author: "曹雪芹",
                    genre: "小说",
                    theme: "历史",
                    cover: "https://picsum.photos/200/300?random=2",
                    tags: ["中国文学", "经典"],
                    description: "描绘清代贵族家庭生活的经典小说。"
                },
                {
                    id: 3,
                    title: "西游记",
                    author: "吴承恩",
                    genre: "小说",
                    theme: "玄幻",
                    cover: "https://picsum.photos/200/300?random=3",
                    tags: ["中国文学", "神话"],
                    description: "讲述孙悟空取经故事的神话小说。"
                },
                {
                    id: 4,
                    title: "诗经",
                    author: "佚名",
                    genre: "诗歌",
                    theme: "历史",
                    cover: "https://picsum.photos/200/300?random=4",
                    tags: ["古典文学", "诗歌"],
                    description: "中国最早的诗歌总集。"
                }
            ];
            books.value = dummyBooks;
            saveToStorage();
        }
    };


    const addBook = (book) => {
        book.id = Date.now();
        books.value.push(book);
        saveToStorage();
    };

    const updateBook = (id, updatedBook) => {
        const index = books.value.findIndex(b => b.id === id);
        if (index !== -1) {
            books.value[index] = { ...books.value[index], ...updatedBook };
            saveToStorage();
        }
    };

    const deleteBook = (id) => {
        books.value = books.value.filter(b => b.id !== id);
        saveToStorage();
    };

    const getBookById = (id) => {
        return books.value.find(b => b.id === id);
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
        const tags = new Set([...customTags.value]);
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

    const addCustomTag = (tag) => {
        const cleaned = tag?.trim();
        if (cleaned && !customTags.value.includes(cleaned)) {
            customTags.value.push(cleaned);
            saveToStorage();
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

    const removeTagFromAllBooks = (tagToRemove) => {
        customTags.value = customTags.value.filter(t => t !== tagToRemove);
        selectedTags.value = selectedTags.value.filter(t => t !== tagToRemove);
        books.value = books.value.map((book) => {
            if (book.tags && Array.isArray(book.tags) && book.tags.includes(tagToRemove)) {
                return { ...book, tags: book.tags.filter((t) => t !== tagToRemove) };
            }
            return book;
        });
        saveToStorage();
    };

    const clearAllFilters = () => {
        searchQuery.value = '';
        selectedGenres.value = [];
        selectedThemes.value = [];
        selectedTags.value = [];
    };

    // Initialize dummy data on store creation
    initializeDummyData();

    return {
        books,
        searchQuery,
        selectedGenres,
        selectedThemes,
        selectedTags,
        allGenres,
        allThemes,
        allTags,
        filteredBooks,
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
        addCustomTag,
        removeCustomGenre,
        removeCustomTheme,
        removeTagFromAllBooks,
        clearAllFilters,
    };
});
