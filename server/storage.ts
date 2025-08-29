import { type User, type InsertUser, type Contribution, type InsertContribution } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByEmail(email: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  getUserContributions(userId: string): Promise<Contribution[]>;
  createContribution(contribution: InsertContribution & { userId: string; filePath?: string; fileSize?: number; mimeType?: string }): Promise<Contribution>;
  getContribution(id: string): Promise<Contribution | undefined>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private contributions: Map<string, Contribution>;

  constructor() {
    this.users = new Map();
    this.contributions = new Map();
    
    // Create a demo user for testing
    const demoUser: User = {
      id: "demo-user-id",
      email: "demo@example.com",
      password: "password123", // In production, this would be hashed
      name: "Demo User",
      createdAt: new Date(),
    };
    this.users.set(demoUser.id, demoUser);

    // Create some demo contributions
    const demoContributions: Contribution[] = [
      {
        id: "contrib-1",
        userId: demoUser.id,
        title: "Telugu Poetry Collection",
        type: "text",
        content: "Sample Telugu poetry content...",
        category: "Literature",
        language: "Telugu",
        description: "A collection of traditional Telugu poems",
        tags: ["poetry", "literature", "telugu"],
        status: "approved",
        createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
        filePath: null,
        fileSize: null,
        mimeType: null,
      },
      {
        id: "contrib-2",
        userId: demoUser.id,
        title: "Audio Pronunciation Guide",
        type: "audio",
        content: null,
        category: "Educational",
        language: "Telugu",
        description: "Pronunciation guide for common Telugu words",
        tags: ["pronunciation", "audio", "educational"],
        status: "processing",
        filePath: "/uploads/audio/pronunciation-guide.mp3",
        fileSize: 2048000,
        mimeType: "audio/mpeg",
        createdAt: new Date(Date.now() - 5 * 60 * 60 * 1000), // 5 hours ago
      },
      {
        id: "contrib-3",
        userId: demoUser.id,
        title: "Cultural Documentary Clips",
        type: "video",
        content: null,
        category: "Cultural",
        language: "Telugu",
        description: "Short clips showcasing Telugu culture",
        tags: ["culture", "documentary", "video"],
        status: "approved",
        filePath: "/uploads/video/cultural-clips.mp4",
        fileSize: 15728640,
        mimeType: "video/mp4",
        createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
      },
    ];

    demoContributions.forEach(contrib => {
      this.contributions.set(contrib.id, contrib);
    });
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.email === email,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { 
      ...insertUser, 
      id,
      createdAt: new Date(),
    };
    this.users.set(id, user);
    return user;
  }

  async getUserContributions(userId: string): Promise<Contribution[]> {
    return Array.from(this.contributions.values())
      .filter(contribution => contribution.userId === userId)
      .sort((a, b) => b.createdAt!.getTime() - a.createdAt!.getTime());
  }

  async createContribution(insertContribution: InsertContribution & { userId: string; filePath?: string; fileSize?: number; mimeType?: string }): Promise<Contribution> {
    const id = randomUUID();
    const contribution: Contribution = {
      ...insertContribution,
      id,
      status: "processing",
      createdAt: new Date(),
      filePath: insertContribution.filePath || null,
      fileSize: insertContribution.fileSize || null,
      mimeType: insertContribution.mimeType || null,
    };
    this.contributions.set(id, contribution);
    return contribution;
  }

  async getContribution(id: string): Promise<Contribution | undefined> {
    return this.contributions.get(id);
  }
}

export const storage = new MemStorage();
