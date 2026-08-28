export type UserRole = "LEA_OFFICER" | "BANK_FI" | "I4C_ANALYST";

export interface User {
  id: string;

  name: string;

  email: string;

  role: UserRole;

  organization?: string;
}

export interface LoginCredentials {
  email: string;

  password: string;

  role: UserRole;
}

export interface LoginResponse {
  user: User;

  token: string;
}