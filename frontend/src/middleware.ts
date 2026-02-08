import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Routes that require authentication
const protectedRoutes = ['/dashboard', '/tasks'];

// Routes that should redirect authenticated users
const authRoutes = ['/sign-in', '/sign-up'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Get the token from cookies
  // Try both cookie name formats for compatibility
  const token = request.cookies.get('auth-token')?.value ||
                request.cookies.get('auth_token')?.value;
  const isAuthenticated = !!token;

  // Debug logging (remove in production)
  console.log('[Middleware]', pathname, 'isAuthenticated:', isAuthenticated, 'token exists:', !!token);

  // Check if the current route is protected
  const isProtectedRoute = protectedRoutes.some(route =>
    pathname.startsWith(route)
  );

  // Check if the current route is an auth route
  const isAuthRoute = authRoutes.some(route =>
    pathname.startsWith(route)
  );

  // Redirect unauthenticated users to sign-in
  if (isProtectedRoute && !isAuthenticated) {
    const signInUrl = new URL('/sign-in', request.url);
    signInUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(signInUrl);
  }

  // Redirect authenticated users away from auth pages
  if (isAuthRoute && isAuthenticated) {
    // Check for redirect parameter
    const redirectUrl = request.nextUrl.searchParams.get('redirect');
    if (redirectUrl) {
      return NextResponse.redirect(new URL(redirectUrl, request.url));
    }
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

// Configure which routes should trigger middleware
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
