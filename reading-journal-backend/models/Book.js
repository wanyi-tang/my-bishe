const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema(
    {
        title: {
            type: String,
            required: [true, 'Please provide a book title'],
            trim: true,
            maxlength: [200, 'Title cannot exceed 200 characters'],
        },
        author: {
            type: String,
            required: [true, 'Please provide an author'],
            trim: true,
            maxlength: [100, 'Author name cannot exceed 100 characters'],
        },
        cover: {
            type: String,
            default: '',
            trim: true,
        },
        genre: {
            type: String,
            enum: [
                '小说',
                '散文',
                '诗歌',
                '戏剧',
                '历史',
                '哲学',
                '科学',
                '传记',
                '其他',
            ],
            default: '其他',
        },
        theme: {
            type: String,
            trim: true,
            maxlength: [100, 'Theme cannot exceed 100 characters'],
        },
        tags: {
            type: [String],
            default: [],
        },
        content: {
            type: String,
            default: '',
            description: 'Rich text content for journal entries',
        },
        rating: {
            type: Number,
            min: 1,
            max: 5,
            default: null,
        },
        readDate: {
            type: Date,
            default: null,
        },
        status: {
            type: String,
            enum: ['想读', '在读', '已读', '弃读'],
            default: '想读',
        },
    },
    {
        timestamps: true, // Adds createdAt and updatedAt automatically
    }
);

// Index for faster queries on common filter fields
bookSchema.index({ genre: 1 });
bookSchema.index({ theme: 1 });
bookSchema.index({ tags: 1 });
bookSchema.index({ status: 1 });

module.exports = mongoose.model('Book', bookSchema);
