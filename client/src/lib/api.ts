// Fetch current user info
export async function getCurrentUser() {
  const response = await apiRequest('/api/v1/auth/me');
  return response.json();
}
import { getAuthHeaders } from "./auth";
import type { LoginCredentials } from "@shared/schema";

const API_BASE_URL = 'https://api.corpus.swecha.org';

async function apiRequest(endpoint: string, options: RequestInit = {}): Promise<Response> {

  const url = API_BASE_URL + endpoint;
  let headers = { ...getAuthHeaders(), ...options.headers };

  // If body is FormData, remove all headers except Authorization so browser sets Content-Type
  if (options.body instanceof FormData) {
    headers = Object.fromEntries(
      Object.entries(headers).filter(([k]) => k.toLowerCase() === 'authorization')
    );
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(errorData.message || `HTTP ${response.status}`);
  }

  return response;
}

export async function loginUser(credentials: LoginCredentials) {
  // The API expects 'phone' instead of 'mobile'
  const payload = { phone: credentials.mobile, password: credentials.password };
  console.log('Login payload:', payload);
  const response = await apiRequest('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  console.log('Login response status:', response.status);
  const data = await response.clone().json().catch(() => ({}));
  console.log('Login response data:', data);
  return data;
}

export async function getUserContributions(userId: string) {
  const response = await apiRequest(`/api/v1/users/${userId}/contributions`);
  // The API returns a structured object, not a flat array
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
