import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { loginSchema, insertContributionSchema } from "@shared/schema";
import { z } from "zod";
import jwt from "jsonwebtoken";
import multer from "multer";
import path from "path";

const JWT_SECRET = process.env.JWT_SECRET || "your-secret-key";

// Configure multer for file uploads
const upload = multer({
  dest: 'uploads/',
  limits: {
    fileSize: 500 * 1024 * 1024, // 500MB limit
  }
});

// Middleware to verify JWT token
function authenticateToken(req: any, res: any, next: any) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err: any, user: any) => {
    if (err) {
      return res.status(403).json({ message: 'Invalid or expired token' });
    }
    req.user = user;
    next();
  });
}

export async function registerRoutes(app: Express): Promise<Server> {
  // Login endpoint
  app.post("/api/v1/auth/login", async (req, res) => {
    try {
      const { mobile, password } = loginSchema.parse(req.body);
      
      const user = await storage.getUserByMobile(mobile);
      if (!user || user.password !== password) {
        return res.status(401).json({ message: "Invalid credentials" });
      }

      const token = jwt.sign(
        { userId: user.id, mobile: user.mobile },
        JWT_SECRET,
        { expiresIn: '24h' }
      );

      res.json({
        token,
        user: {
          id: user.id,
          mobile: user.mobile,
          name: user.name,
        }
      });
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid input", errors: error.errors });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get user contributions
  app.get("/api/v1/users/:userId/contributions", authenticateToken, async (req, res) => {
    try {
      const { userId } = req.params;
      
      // Ensure user can only access their own contributions
      if (req.user.userId !== userId) {
        return res.status(403).json({ message: "Access denied" });
      }

      const contributions = await storage.getUserContributions(userId);
      res.json(contributions);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Upload record (for text and images)
  app.post("/api/v1/records/upload", authenticateToken, upload.single('file'), async (req, res) => {
    try {
      const contributionData = {
        ...req.body,
        userId: req.user.userId,
      };

      // Handle file upload if present
      if (req.file) {
        contributionData.filePath = req.file.path;
        contributionData.fileSize = req.file.size;
        contributionData.mimeType = req.file.mimetype;
      }

      // Parse tags if they're a string
      if (typeof contributionData.tags === 'string') {
        contributionData.tags = contributionData.tags.split(',').map((tag: string) => tag.trim());
      }

      const validatedData = insertContributionSchema.extend({
        userId: z.string(),
        filePath: z.string().optional(),
        fileSize: z.number().optional(),
        mimeType: z.string().optional(),
      }).parse(contributionData);

      const contribution = await storage.createContribution(validatedData);
      res.status(201).json(contribution);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid input", errors: error.errors });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Upload chunk (for audio and video)
  app.post("/api/v1/records/upload/chunk", authenticateToken, upload.single('file'), async (req, res) => {
    try {
      const contributionData = {
        ...req.body,
        userId: req.user.userId,
      };

      // Handle chunked file upload
      if (req.file) {
        contributionData.filePath = req.file.path;
        contributionData.fileSize = req.file.size;
        contributionData.mimeType = req.file.mimetype;
      }

      // Parse tags if they're a string
      if (typeof contributionData.tags === 'string') {
        contributionData.tags = contributionData.tags.split(',').map((tag: string) => tag.trim());
      }

      const validatedData = insertContributionSchema.extend({
        userId: z.string(),
        filePath: z.string().optional(),
        fileSize: z.number().optional(),
        mimeType: z.string().optional(),
      }).parse(contributionData);

      const contribution = await storage.createContribution(validatedData);
      res.status(201).json(contribution);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid input", errors: error.errors });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
