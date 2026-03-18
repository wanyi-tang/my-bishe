import apiClient from './bookApi';

/**
 * Books API Service
 * Provides methods to interact with the backend books API
 */
export const bookApi = {
  /**
   * Get all books with optional filters
   * @param {Object} params - Query parameters
   * @param {string} [params.search] - Search keyword
   * @param {string} [params.genre] - Filter by genre
   * @returns {Promise<Array>} List of books
   */
  async getAllBooks(params = {}) {
    const response = await apiClient.get('/books', { params });
    return response;
  },

  /**
   * Get a single book by ID
   * @param {string} id - Book ID
   * @returns {Promise<Object>} Book object
   */
  async getBookById(id) {
    const response = await apiClient.get(`/books/${id}`);
    return response;
  },

  /**
   * Create a new book
   * @param {Object} bookData - Book data
   * @returns {Promise<Object>} Created book object
   */
  async createBook(bookData) {
    const response = await apiClient.post('/books', bookData);
    return response;
  },

  /**
   * Update an existing book
   * @param {string} id - Book ID
   * @param {Object} bookData - Updated book data
   * @returns {Promise<Object>} Updated book object
   */
  async updateBook(id, bookData) {
    const response = await apiClient.put(`/books/${id}`, bookData);
    return response;
  },

  /**
   * Delete a book
   * @param {string} id - Book ID
   * @returns {Promise<void>}
   */
  async deleteBook(id) {
    const response = await apiClient.delete(`/books/${id}`);
    return response;
  },
};

export default bookApi;
