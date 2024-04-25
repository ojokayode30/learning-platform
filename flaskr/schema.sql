-- Create database (SQLite does not require explicit creation of the database)
-- Removed: CREATE DATABASE ai_learning_platform;
DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS courses;

DROP TABLE IF EXISTS lessons;

DROP TABLE IF EXISTS user_course_enrollment;

DROP TABLE IF EXISTS user_lesson_progress;

DROP TABLE IF EXISTS lesson_comments;

DROP TABLE IF EXISTS ai_models;

DROP TABLE IF EXISTS training_data;

DROP TABLE IF EXISTS predictions;

DROP TABLE IF EXISTS evaluations;

DROP TABLE IF EXISTS chat_conversations;

DROP TABLE IF EXISTS chat_messages;

DROP TABLE IF EXISTS chat_participants;

-- Table for users
CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

-- Table for courses
CREATE TABLE
    courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        instructor VARCHAR(100),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

-- Table for lessons
CREATE TABLE
    lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id CHAR(36),
        title VARCHAR(255) NOT NULL,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    );

-- Table for user-course enrollment (many-to-many relationship)
CREATE TABLE
    user_course_enrollment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(36),
        course_id CHAR(36),
        enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    );

-- Table for tracking user progress in lessons
CREATE TABLE
    user_lesson_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(36),
        lesson_id CHAR(36),
        completed BOOLEAN DEFAULT 0,
        progress_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE
    );

-- Table for comments/discussion
CREATE TABLE
    lesson_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(36),
        lesson_id CHAR(36),
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE
    );

-- Table for AI models
CREATE TABLE
    ai_models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

-- Table for training data
CREATE TABLE
    training_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ai_model_id CHAR(36),
        data TEXT,
        label TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ai_model_id) REFERENCES ai_models (id) ON DELETE CASCADE
    );

-- Table for predictions
CREATE TABLE
    predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ai_model_id CHAR(36),
        data TEXT,
        prediction TEXT,
        confidence FLOAT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ai_model_id) REFERENCES ai_models (id) ON DELETE CASCADE
    );

-- Table for evaluations
CREATE TABLE
    evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ai_model_id CHAR(36),
        evaluation_metric VARCHAR(100),
        value FLOAT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ai_model_id) REFERENCES ai_models (id) ON DELETE CASCADE
    );

-- Table for chat conversations
CREATE TABLE
    chat_conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255), -- Optional
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

-- Table for chat messages
CREATE TABLE
    chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id CHAR(36),
        sender_id CHAR(36), -- User or lecturer ID
        message_content TEXT,
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES chat_conversations (id) ON DELETE CASCADE
    );

-- Table for participants
CREATE TABLE
    chat_participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id CHAR(36),
        participant_type TEXT CHECK (participant_type IN ('user', 'lecturer')),
        participant_id CHAR(36), -- User or lecturer ID
        FOREIGN KEY (conversation_id) REFERENCES chat_conversations (id) ON DELETE CASCADE
    );

-- Insert sample data into the courses table
INSERT INTO
    users (first_name, last_name, email, username, password)
VALUES
    (
        'Kayode',
        'Ojo',
        'k.ojo@mail.com',
        'kojo',
        'scrypt:32768:8:1$Mo6bKWd5fYglpvBT$30c8dac2b9982b74c1f7d3d1e6bfc4e1040d3b0f1ad8b6a4efcb5929f0342537fab78ab278d2b8f92935e6a6e486e0e8328770cad0e8795b717391ed8c63653a'
    ),
    (
        'John',
        'Doe',
        'john@example.com',
        'johndoe',
        'scrypt:32768:8:1$Mo6bKWd5fYglpvBT$30c8dac2b9982b74c1f7d3d1e6bfc4e1040d3b0f1ad8b6a4efcb5929f0342537fab78ab278d2b8f92935e6a6e486e0e8328770cad0e8795b717391ed8c63653a'
    ),
    (
        'Alice',
        'Smith',
        'alice@example.com',
        'alicesmith',
        'scrypt:32768:8:1$Mo6bKWd5fYglpvBT$30c8dac2b9982b74c1f7d3d1e6bfc4e1040d3b0f1ad8b6a4efcb5929f0342537fab78ab278d2b8f92935e6a6e486e0e8328770cad0e8795b717391ed8c63653a'
    ),
    (
        'Bob',
        'Johnson',
        'bob@example.com',
        'bobjohnson',
        'scrypt:32768:8:1$Mo6bKWd5fYglpvBT$30c8dac2b9982b74c1f7d3d1e6bfc4e1040d3b0f1ad8b6a4efcb5929f0342537fab78ab278d2b8f92935e6a6e486e0e8328770cad0e8795b717391ed8c63653a'
    );

-- Insert sample data into the courses table
INSERT INTO
    courses (
        title,
        description,
        instructor,
        created_at,
        updated_at
    )
VALUES
    (
        'Introduction to Machine Learning',
        'Learn the basics of machine learning algorithms and techniques.',
        'Dr. John Smith',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        'Deep Learning Fundamentals',
        'Explore deep neural networks, convolutional neural networks (CNNs), and recurrent neural networks (RNNs).',
        'Prof. Sarah Johnson',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        'Natural Language Processing',
        'Study techniques for processing and analyzing human language data.',
        'Dr. Michael Brown',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        'Computer Vision',
        'Learn about image processing, object detection, and image classification using deep learning models.',
        'Dr. Emily White',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        'Reinforcement Learning',
        'Understand the principles and algorithms behind reinforcement learning.',
        'Prof. David Jones',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );

INSERT INTO
    lessons (course_id, title, content)
VALUES
    (
        '2',
        'Introduction to Deep Learning',
        'An overview of deep learning and its applications.'
    ),
    (
        '2',
        'Neural Networks Basics',
        'Understanding the building blocks of neural networks.'
    ),
    (
        '2',
        'Gradient Descent Optimization',
        'Exploring gradient descent algorithms for optimization.'
    ),
    (
        '2',
        'Convolutional Neural Networks (CNNs)',
        'Introduction to CNNs and their applications in image recognition.'
    ),
    (
        '2',
        'Recurrent Neural Networks (RNNs)',
        'Understanding RNNs and their applications in sequential data analysis.'
    ),
    (
        '2',
        'Deep Learning Frameworks',
        'An overview of popular deep learning frameworks like TensorFlow and PyTorch.'
    );

INSERT INTO
    lessons (course_id, title, content)
VALUES
    (
        '1',
        'Introduction to Machine Learning',
        'An overview of machine learning concepts and applications.'
    ),
    (
        '1',
        'Supervised Learning',
        'Understanding supervised learning algorithms and techniques.'
    ),
    (
        '1',
        'Unsupervised Learning',
        'Exploring unsupervised learning algorithms and techniques.'
    ),
    (
        '1',
        'Feature Engineering',
        'Techniques for feature selection, extraction, and transformation.'
    ),
    (
        '1',
        'Model Evaluation and Validation',
        'Methods for evaluating and validating machine learning models.'
    ),
    (
        '1',
        'Model Deployment',
        'Considerations and best practices for deploying machine learning models in production.'
    );