// T025: useAuth custom hook

'use client';

import { useAuthContext } from '@/lib/auth-context';

/**
 * Hook to access authentication state and methods
 * Must be used within AuthProvider
 */
export const useAuth = () => {
  return useAuthContext();
};
