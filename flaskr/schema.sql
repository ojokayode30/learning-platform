-- Create database (SQLite does not require explicit creation of the database)
-- Removed: CREATE DATABASE ai_learning_platform;

-- Table for users
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for courses
CREATE TABLE courses (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructor VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for lessons
CREATE TABLE lessons (
    id CHAR(36) PRIMARY KEY,
    course_id CHAR(36),
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Table for user-course enrollment (many-to-many relationship)
CREATE TABLE user_course_enrollment (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    course_id CHAR(36),
    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Table for tracking user progress in lessons
CREATE TABLE user_lesson_progress (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    lesson_id CHAR(36),
    completed BOOLEAN DEFAULT 0,
    progress_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
);

-- Table for comments/discussion
CREATE TABLE lesson_comments (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    lesson_id CHAR(36),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
);

-- Table for AI models
CREATE TABLE ai_models (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for training data
CREATE TABLE training_data (
    id CHAR(36) PRIMARY KEY,
    ai_model_id CHAR(36),
    data TEXT,
    label TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ai_model_id) REFERENCES ai_models(id) ON DELETE CASCADE
);

-- Table for predictions
CREATE TABLE predictions (
    id CHAR(36) PRIMARY KEY,
    ai_model_id CHAR(36),
    data TEXT,
    prediction TEXT,
    confidence FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ai_model_id) REFERENCES ai_models(id) ON DELETE CASCADE
);

-- Table for evaluations
CREATE TABLE evaluations (
    id CHAR(36) PRIMARY KEY,
    ai_model_id CHAR(36),
    evaluation_metric VARCHAR(100),
    value FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ai_model_id) REFERENCES ai_models(id) ON DELETE CASCADE
);

-- Table for chat conversations
CREATE TABLE chat_conversations (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255), -- Optional
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for chat messages
CREATE TABLE chat_messages (
    id CHAR(36) PRIMARY KEY,
    conversation_id CHAR(36),
    sender_id CHAR(36), -- User or lecturer ID
    message_content TEXT,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES chat_conversations(id) ON DELETE CASCADE
);

-- Table for participants
CREATE TABLE chat_participants (
    id CHAR(36) PRIMARY KEY,
    conversation_id CHAR(36),
    participant_type TEXT CHECK(participant_type IN ('user', 'lecturer')),
    participant_id CHAR(36), -- User or lecturer ID
    FOREIGN KEY (conversation_id) REFERENCES chat_conversations(id) ON DELETE CASCADE
);
