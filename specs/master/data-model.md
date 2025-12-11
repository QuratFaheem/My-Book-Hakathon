# Data Model: Physical AI & Humanoid Robotics Textbook

## Overview

This document defines the data models for the Physical AI & Humanoid Robotics Textbook project, including both the documentation content structure and the RAG chatbot backend data structures.

## Content Data Model

### Chapter
- id: string (unique identifier)
- title: string (chapter title)
- slug: string (URL-friendly identifier)
- content: string (Markdown content)
- order: integer (sequence in the textbook)
- sections: array of Section objects
- prerequisites: array of Chapter IDs
- learning_objectives: array of strings
- created_at: datetime
- updated_at: datetime

### Section
- id: string (unique identifier)
- title: string (section title)
- content: string (Markdown content)
- order: integer (sequence within chapter)
- chapter_id: string (foreign key to Chapter)
- examples: array of Example objects

### Example
- id: string (unique identifier)
- title: string (example title)
- description: string (brief explanation)
- code: string (executable code block)
- language: string (programming language)
- chapter_id: string (foreign key to Chapter)
- section_id: string (foreign key to Section)

## RAG Backend Data Model

### User
- id: string (unique identifier, UUID)
- email: string (email address)
- username: string (optional)
- preferences: JSON (language, accessibility settings)
- created_at: datetime
- updated_at: datetime

### Document
- id: string (unique identifier)
- title: string (document title)
- content: string (full text content)
- source_path: string (path in docs directory)
- embedding: vector (Qdrant vector representation)
- metadata: JSON (additional information like chapter, section)
- created_at: datetime
- updated_at: datetime

### ChatSession
- id: string (unique identifier)
- user_id: string (foreign key to User, optional for anonymous)
- created_at: datetime
- updated_at: datetime
- title: string (brief session summary)

### ChatMessage
- id: string (unique identifier)
- session_id: string (foreign key to ChatSession)
- role: string (user or assistant)
- content: string (message text)
- timestamp: datetime
- context_chunks: array of Document IDs (relevant context for the response)
- model_used: string (name of the model used)