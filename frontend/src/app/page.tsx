// Root page - redirects to appropriate destination

import { redirect } from 'next/navigation';

export default function Home() {
  // Redirect to sign-in page by default
  // Middleware will handle redirecting authenticated users to dashboard
  redirect('/sign-in');
}
