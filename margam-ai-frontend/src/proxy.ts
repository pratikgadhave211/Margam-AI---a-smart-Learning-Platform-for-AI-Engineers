import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export default function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Protect all routes under /questions
  if (pathname.startsWith('/questions')) {
    // Better Auth stores the session token in a cookie
    const hasToken = request.cookies.get('better-auth.session_token') || 
                     request.cookies.get('__Secure-better-auth.session_token');
                     
    if (!hasToken) {
      // If no token is found, redirect instantly to login page
      return NextResponse.redirect(new URL('/auth', request.url));
    }
  }
  
  return NextResponse.next();
}

// Only run middleware on question routes to optimize performance
export const config = {
  matcher: ['/questions/:path*'],
};
