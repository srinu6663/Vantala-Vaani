# Overview

This is a full-stack TypeScript web application for cultural content contribution and management, specifically designed for Telugu language materials. The application allows users to upload and manage various types of cultural content including text, audio, video, and images. It features a modern React frontend with shadcn/ui components and an Express.js backend with PostgreSQL database integration using Drizzle ORM.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: React 18 with TypeScript using Vite as the build tool
- **UI Components**: shadcn/ui component library built on Radix UI primitives
- **Styling**: Tailwind CSS with custom CSS variables for theming
- **State Management**: TanStack React Query for server state and local React state for UI
- **Routing**: Wouter for lightweight client-side routing
- **Forms**: React Hook Form with Zod validation for type-safe form handling

## Backend Architecture
- **Runtime**: Node.js with Express.js framework
- **Language**: TypeScript with ES modules
- **API Design**: RESTful API with structured route organization
- **File Uploads**: Multer middleware for handling multipart form data with 500MB file size limit
- **Authentication**: JWT-based authentication with Bearer token strategy
- **Error Handling**: Centralized error handling middleware with structured error responses

## Database Layer
- **ORM**: Drizzle ORM for type-safe database operations
- **Database**: PostgreSQL with Neon Database serverless hosting
- **Schema Management**: Drizzle Kit for migrations and schema management
- **Connection**: Connection pooling through @neondatabase/serverless driver

## Authentication & Authorization
- **Strategy**: JWT token-based authentication
- **Storage**: Browser localStorage for token persistence
- **Middleware**: Custom authentication middleware for protected routes
- **Session Management**: Stateless authentication with configurable token expiration

## Data Storage Solutions
- **Primary Database**: PostgreSQL for structured data (users, contributions, metadata)
- **File Storage**: Local filesystem with configurable upload directory
- **In-Memory Fallback**: MemStorage class for development/testing with demo data
- **Content Types**: Support for text, audio, video, and image content with appropriate metadata

## Development & Build Process
- **Development**: Vite dev server with HMR and TypeScript compilation
- **Build**: Separate client and server builds with esbuild for server bundling
- **Environment**: Environment-based configuration with NODE_ENV detection
- **Database Operations**: Push-based schema deployment with Drizzle Kit

## Project Structure
- **Monorepo Layout**: Shared schema and utilities between client and server
- **Client Directory**: React frontend application with component-based architecture
- **Server Directory**: Express.js backend with route-based organization
- **Shared Directory**: Common TypeScript types and Zod schemas for validation

# External Dependencies

## Core Framework Dependencies
- **React Ecosystem**: React 18, React DOM, React Hook Form for frontend functionality
- **Express.js**: Web application framework for Node.js backend
- **TypeScript**: Static type checking across the entire application stack

## Database & ORM
- **Drizzle ORM**: Modern TypeScript ORM for database operations
- **Neon Database**: Serverless PostgreSQL hosting solution
- **Drizzle Kit**: Database migration and schema management tools

## UI Component Libraries
- **Radix UI**: Headless, accessible UI primitives for React
- **Lucide React**: Modern icon library with consistent design
- **Tailwind CSS**: Utility-first CSS framework for rapid styling

## Authentication & Security
- **jsonwebtoken**: JWT token generation and verification
- **Zod**: Runtime type validation and schema parsing

## File Handling
- **Multer**: Node.js middleware for handling multipart/form-data uploads
- **File System**: Native Node.js fs module for file operations

## Development Tools
- **Vite**: Fast build tool and development server
- **esbuild**: JavaScript bundler for production server builds
- **tsx**: TypeScript execution engine for Node.js development

## State Management & Data Fetching
- **TanStack React Query**: Powerful data synchronization for React applications
- **Wouter**: Minimalist routing library for React applications

## Validation & Forms
- **Zod**: TypeScript-first schema validation library
- **Hookform Resolvers**: Integration layer between React Hook Form and validation libraries