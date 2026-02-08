// T015: TypeScript types for Auth entities

export interface User {
  id: string;
  email: string;
}

export interface AuthUser {
  id: string;
  email: string;
  createdAt: string;
}

export interface AuthResponse {
  user: AuthUser;
  token: string;
}

export interface LoginResponse {
  user: AuthUser;
  token: string;
}

export interface RegisterResponse {
  user: AuthUser;
  token: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LogoutResponse {
  message: string;
}

export interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  signUp: (email: string, password: string) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  clearError: () => void;
}

export interface JWTPayload {
  sub: string;
  email: string;
  iat: number;
  exp: number;
}
