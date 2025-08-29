import { getAuthHeaders } from "./auth";
import type { LoginCredentials } from "@shared/schema";

const API_BASE_URL = '';

async function apiRequest(endpoint: string, options: RequestInit = {}): Promise<Response> {
  const url = API_BASE_URL + endpoint;
  const response = await fetch(url, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(errorData.message || `HTTP ${response.status}`);
  }

  return response;
}

export async function loginUser(credentials: LoginCredentials) {
  const response = await apiRequest('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  return response.json();
}

export async function getUserContributions(userId: string) {
  const response = await apiRequest(`/api/v1/users/${userId}/contributions`);
  return response.json();
}

export async function uploadRecord(formData: FormData) {
  const response = await apiRequest('/api/v1/records/upload', {
    method: 'POST',
    body: formData,
  });

  return response.json();
}

export async function uploadChunk(formData: FormData) {
  const response = await apiRequest('/api/v1/records/upload/chunk', {
    method: 'POST',
    body: formData,
  });

  return response.json();
}
