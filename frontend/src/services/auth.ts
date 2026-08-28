import type {
  LoginCredentials,
  User,
} from "../types/user";

import {
  authenticateMockUser,
} from "../mocks/users";

const AUTH_STORAGE_KEY =
  "cybersentinel_auth";

const USE_MOCK_AUTH = true;

interface StoredAuth {
  user: User;
  token: string;
}

export const login = async (
  credentials: LoginCredentials,
): Promise<StoredAuth> => {
  if (USE_MOCK_AUTH) {
    await new Promise((resolve) =>
      setTimeout(resolve, 500),
    );

    const user =
      authenticateMockUser(credentials);

    if (!user) {
      throw new Error(
        "Invalid email, password, or role.",
      );
    }

    const auth: StoredAuth = {
      user,
      token: `mock-token-${user.id}`,
    };

    localStorage.setItem(
      AUTH_STORAGE_KEY,
      JSON.stringify(auth),
    );

    return auth;
  }

  throw new Error(
    "Real authentication API is not enabled.",
  );
};

export const getStoredAuth =
  (): StoredAuth | null => {
    try {
      const stored =
        localStorage.getItem(
          AUTH_STORAGE_KEY,
        );

      if (!stored) {
        return null;
      }

      return JSON.parse(
        stored,
      ) as StoredAuth;
    } catch {
      localStorage.removeItem(
        AUTH_STORAGE_KEY,
      );

      return null;
    }
  };

export const getCurrentUser =
  (): User | null => {
    return getStoredAuth()?.user ?? null;
  };

export const isAuthenticated =
  (): boolean => {
    return Boolean(getStoredAuth());
  };

export const logout = (): void => {
  localStorage.removeItem(
    AUTH_STORAGE_KEY,
  );
};