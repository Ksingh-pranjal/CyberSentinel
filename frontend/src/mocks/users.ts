import type {
  LoginCredentials,
  User,
} from "../types/user";

export const mockUsers: User[] = [
  {
    id: "USR-001",
    name: "Arjun Sharma",
    email: "officer@demo.gov",
    role: "LEA_OFFICER",
    organization: "Law Enforcement Agency",
  },

  {
    id: "USR-002",
    name: "Priya Mehta",
    email: "analyst@demo.gov",
    role: "I4C_ANALYST",
    organization: "Indian Cyber Crime Coordination Centre",
  },

  {
    id: "USR-003",
    name: "Rahul Verma",
    email: "bank@demo.gov",
    role: "BANK_FI",
    organization: "Financial Institution",
  },
];

export const MOCK_PASSWORD = "demo123";

export const authenticateMockUser = (
  credentials: LoginCredentials,
): User | null => {
  const user = mockUsers.find(
    (candidate) =>
      candidate.email.toLowerCase() ===
        credentials.email.toLowerCase() &&
      candidate.role === credentials.role,
  );

  if (!user) {
    return null;
  }

  if (credentials.password !== MOCK_PASSWORD) {
    return null;
  }

  return user;
};

export const getMockUserById = (
  id: string,
): User | undefined => {
  return mockUsers.find(
    (user) => user.id === id,
  );
};