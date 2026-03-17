# README_DEV.md
## Personal Reading Journal System - Developer Guide

This file describes the development rules and architecture for this project.

This project is a **graduation design prototype system**.

The goal is to build a **Personal Reading Journal System** that allows users to manage books, write reading notes, and visualize reading data.

The system follows **frontend-backend separation architecture**.

---

# Tech Stack

Frontend

- Vue 3
- Vite
- Vue Router
- Pinia
- Axios
- Tiptap Editor
- ECharts

Backend

- Spring Boot
- Spring Data JPA
- RESTful API
- Maven

Database

- MySQL

---

# Project Architecture

Frontend

Single Page Application using Vue 3.

Directory structure:

src
components
views
router
stores
api
assets

Main pages

- Login
- Register
- Dashboard
- Book List
- Book Detail
- Note Editor
- Statistics Dashboard

---

Backend

Spring Boot layered architecture.

Packages should follow this structure:

controller
service
repository
entity
dto
config

Flow

Controller → Service → Repository → Database

---

# Core Modules

The system contains the following modules.

---

# User Module

Responsible for user authentication.

Features

- User registration
- User login
- Authentication
- User profile

Entity

User

Fields

id
username
email
password
createdAt

---

# Book Module

Users can manage their personal book library.

Features

- Add book
- Edit book
- Delete book
- List books
- Book categories
- ISBN input
- Cover image

Entity

Book

Fields

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

# Note Module (Core Feature)

Users can create reading journals linked to books.

Editor technology

Tiptap rich text editor.

Features

- Rich text editing
- Insert images
- Format text
- Scrapbook style layout
- Link note to book

Entity

Note

Fields

id
title
content
bookId
userId
createdAt
updatedAt

Content format

HTML or JSON.

---

# Tag Module

Tags help organize notes.

Features

- Add tags to notes
- Filter notes by tags
- Tag management

Entities

Tag

Fields

id
name

Relation table

NoteTag

Fields

noteId
tagId

Relationship

Note N:N Tag

---

# Search Module

Users can search for content.

Search targets

- Book title
- Note title
- Note content
- Tags

Implementation

Use SQL LIKE search.

Future extension

ElasticSearch.

---

# Statistics Module

The system provides a reading statistics dashboard.

Data sources

- Total books
- Total notes
- Books by category
- Notes created per month

Charts

- Pie chart
- Bar chart
- Line chart

Visualization library

ECharts.

---

# Database Tables

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

# REST API Design

Authentication

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

# Coding Rules

Frontend

Use Vue 3 Composition API.

Use `<script setup>` syntax.

Use Pinia for global state.

Use Axios for API calls.

Component based architecture.

---

Backend

Use layered architecture.

Controller handles HTTP requests.

Service contains business logic.

Repository handles database access.

Use DTO for API responses.

Use Lombok for entity classes.

---

# Development Priority

Develop modules in this order.

1. User authentication
2. Book management
3. Note module
4. Tiptap editor integration
5. Tag system
6. Search function
7. Statistics dashboard

---

# Copilot Instructions

When generating code:

Follow the architecture defined in this document.

Use RESTful API conventions.

Ensure entities match database tables.

Follow Java Spring Boot best practices.

Use Vue 3 Composition API for frontend code.

Generate modular and maintainable code.