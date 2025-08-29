import { sql } from "drizzle-orm";
import { pgTable, text, varchar, timestamp, integer, json } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  email: text("email").notNull().unique(),
  password: text("password").notNull(),
  name: text("name").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const contributions = pgTable("contributions", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").notNull().references(() => users.id),
  title: text("title").notNull(),
  type: text("type").notNull(), // 'text', 'audio', 'video', 'image'
  content: text("content"), // For text content
  filePath: text("file_path"), // For uploaded files
  fileSize: integer("file_size"),
  mimeType: text("mime_type"),
  category: text("category"),
  language: text("language"),
  description: text("description"),
  tags: json("tags").$type<string[]>(),
  status: text("status").notNull().default('processing'), // 'processing', 'approved', 'rejected'
  createdAt: timestamp("created_at").defaultNow(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  email: true,
  password: true,
  name: true,
});

export const insertContributionSchema = createInsertSchema(contributions).pick({
  title: true,
  type: true,
  content: true,
  category: true,
  language: true,
  description: true,
  tags: true,
});

export const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type InsertContribution = z.infer<typeof insertContributionSchema>;
export type Contribution = typeof contributions.$inferSelect;
export type LoginCredentials = z.infer<typeof loginSchema>;
