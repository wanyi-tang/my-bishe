const Book = require('../models/Book');

// @desc    Get all books with optional filtering
// @route   GET /api/books
// @access  Public
const getBooks = async (req, res) => {
    try {
        const { genre, theme, tags, search, status } = req.query;

        // Build query object
        const query = {};

        if (genre) {
            query.genre = genre;
        }

        if (theme) {
            query.theme = new RegExp(theme, 'i'); // Case-insensitive regex search
        }

        if (tags) {
            const tagArray = Array.isArray(tags) ? tags : tags.split(',');
            query.tags = { $in: tagArray };
        }

        if (search) {
            query.$or = [
                { title: new RegExp(search, 'i') },
                { author: new RegExp(search, 'i') },
            ];
        }

        if (status) {
            query.status = status;
        }

        const books = await Book.find(query).sort({ createdAt: -1 });

        res.status(200).json({
            success: true,
            count: books.length,
            data: books,
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error while fetching books',
            error: error.message,
        });
    }
};

// @desc    Get single book by ID
// @route   GET /api/books/:id
// @access  Public
const getBookById = async (req, res) => {
    try {
        const book = await Book.findById(req.params.id);

        if (!book) {
            return res.status(404).json({
                success: false,
                message: `Book not found with id of ${req.params.id}`,
            });
        }

        res.status(200).json({
            success: true,
            data: book,
        });
    } catch (error) {
        if (error.kind === 'ObjectId') {
            return res.status(404).json({
                success: false,
                message: `Book not found with id of ${req.params.id}`,
            });
        }

        res.status(500).json({
            success: false,
            message: 'Server error while fetching book',
            error: error.message,
        });
    }
};

// @desc    Create new book
// @route   POST /api/books
// @access  Public
const createBook = async (req, res) => {
    try {
        const book = await Book.create(req.body);

        res.status(201).json({
            success: true,
            data: book,
        });
    } catch (error) {
        if (error.name === 'ValidationError') {
            const messages = Object.values(error.errors).map(val => val.message);
            return res.status(400).json({
                success: false,
                message: 'Validation error',
                errors: messages,
            });
        }

        res.status(500).json({
            success: false,
            message: 'Server error while creating book',
            error: error.message,
        });
    }
};

// @desc    Update book
// @route   PUT /api/books/:id
// @access  Public
const updateBook = async (req, res) => {
    try {
        let book = await Book.findById(req.params.id);

        if (!book) {
            return res.status(404).json({
                success: false,
                message: `Book not found with id of ${req.params.id}`,
            });
        }

        book = await Book.findByIdAndUpdate(req.params.id, req.body, {
            new: true,
            runValidators: true,
        });

        res.status(200).json({
            success: true,
            data: book,
        });
    } catch (error) {
        if (error.kind === 'ObjectId') {
            return res.status(404).json({
                success: false,
                message: `Book not found with id of ${req.params.id}`,
            });
        }

        if (error.name === 'ValidationError') {
            const messages = Object.values(error.errors).map(val => val.message);
            return res.status(400).json({
                success: false,
                message: 'Validation error',
                errors: messages,
            });
        }

        res.status(500).json({
            success: false,
            message: 'Server error while updating book',
            error: error.message,
        });
    }
};

// @desc    Delete book
// @route   DELETE /api/books/:id
// @access  Public
const deleteBook = async (req, res) => {
    try {
        const book = await Book.findById(req.params.id);

        if (!book) {
            return res.status(404).json({
                success: false,
                message: `Book not found with id of ${req.params.id}`,
            });
        }

        await book.deleteOne();

        res.status(200).json({
            success: true,
            message: 'Book deleted successfully',
        });
    } catch (error) {
        if (error.kind === 'ObjectId') {
            return res.status(404).json({
                success: false,
                message: `Book not found with id of ${req.params.id}`,
            });
        }

        res.status(500).json({
            success: false,
            message: 'Server error while deleting book',
            error: error.message,
        });
    }
};

module.exports = {
    getBooks,
    getBookById,
    createBook,
    updateBook,
    deleteBook,
};
