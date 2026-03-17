# Copilot Project Instructions
## Personal Reading Journal System

This project is a graduation design project.

Project name:
Personal Reading Journal System

The goal is to build a Web application that allows users to manage books, write reading journals, and analyze reading data.

The system combines:

- Personal book management
- Scrapbook-style reading notes
- Knowledge management
- Reading data visualization

This is a prototype system for a university graduation project.

---

# Tech Stack

Frontend

- Vue 3
- Vue Router
- Pinia
- Axios
- Tiptap editor
- ECharts
- Vite

Backend

- Spring Boot
- RESTful API
- Spring Data JPA or MyBatis
- Maven

Database

- MySQL

Architecture

Frontend and backend separated architecture.

---

# System Modules

The system contains the following core modules.

---

# 1 User System

Features:

- User registration
- User login
- Authentication
- User profile

Entity example

User

fields

id
username
email
password
createdAt

---

# 2 Book Management

Users can manage their personal library.

Features

- Add book
- Edit book
- Delete book
- View book list
- Book categories
- ISBN input
- Book cover image

Entity

Book

fields

id
title
author
isbn
coverUrl
description
category
createdAt
userId

Relationship

One user can have many books.

---

# 3 Reading Journal (Core Feature)

This is the most important module.

Users can create scrapbook-style reading journals.

Features

- Rich text editing
- Image insertion
- Text formatting
- Scrapbook style layout
- Book related notes

Editor technology

Tiptap editor

Entity

Note

fields

id
title
content
bookId
userId
createdAt
updatedAt

The content field can store HTML or JSON.

---

# 4 Tag System

Tags are used for knowledge organization.

Features

- Add tag to notes
- Filter notes by tag
- Tag management

Entities

Tag

fields

id
name

Relationship table

NoteTag

fields

noteId
tagId

---

# 5 Search System

The system supports searching.

Search scope

- Book title
- Note title
- Note content
- Tags

Basic implementation

Use SQL LIKE queries.

Future extension

ElasticSearch.

---

# 6 Reading Statistics

The system provides a statistics dashboard.

Statistics include

- Total books
- Total notes
- Books by category
- Monthly note creation
- Reading habits

Visualization library

ECharts

Charts include

- Pie chart
- Bar chart
- Line chart

---

# Database Tables

tables

users
books
notes
tags
note_tags

Relationships

User 1:N Book

User 1:N Note

Book 1:N Note

Note N:N Tag

---

# REST API Style

Use RESTful API design.

Examples

Auth

POST /api/auth/register
POST /api/auth/login

Books

GET /api/books
POST /api/books
GET /api/books/{id}
PUT /api/books/{id}
DELETE /api/books/{id}

Notes

GET /api/notes
POST /api/notes
GET /api/notes/{id}
PUT /api/notes/{id}
DELETE /api/notes/{id}

Tags

GET /api/tags
POST /api/tags

---

# Frontend Structure

src

components
views
router
stores
api
assets

Important components

BookList
BookCard
NoteEditor
TagSelector
StatisticsDashboard

---

# Backend Structure

controller
service
repository
entity
dto
config

---

# Coding Requirements

Frontend

Use Vue 3 Composition API.

Use script setup syntax.

Use Pinia for state management.

Backend

Use layered architecture.

Controller -> Service -> Repository.

Use DTO objects for API responses.

Use Lombok for entity classes.

---

# Development Priority

The system should be implemented in this order.

1 User system

2 Book management

3 Note system

4 Tiptap editor integration

5 Tag system

6 Search function

7 Data visualization dashboard

---

# Project Goal

The final system should be a running Web application that demonstrates:

- Personal book library management
- Reading journal writing
- Book-note relationships
- Knowledge organization with tags
- Reading statistics dashboard

The project focuses on demonstrating software engineering practice, system design, and prototype implementation.