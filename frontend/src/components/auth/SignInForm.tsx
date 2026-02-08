// T027: Sign-in form component with React Hook Form validation

'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { useAuth } from '@/hooks/useAuth';

const signInSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z
    .string()
    .min(1, 'Password is required'),
});

type SignInFormData = z.infer<typeof signInSchema>;

const SignInForm: React.FC = () => {
  const { login, isLoading } = useAuth();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignInFormData>({
    resolver: zodResolver(signInSchema),
  });

  const onSubmit = async (data: SignInFormData) => {
    setServerError(null);

    try {
      await login(data.email, data.password);
    } catch (error) {
      if (error instanceof Error) {
        setServerError(error.message);
      } else {
        setServerError('Failed to sign in. Please try again.');
      }
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Welcome Back
          </h1>
          <p className="text-sm text-gray-600">
            Sign in to continue to your tasks
          </p>
        </div>

        {serverError && (
          <div
            className="mb-4 p-3 bg-error-50 border border-error-200 rounded-lg"
            role="alert"
          >
            <p className="text-sm text-error-700">{serverError}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <Input
            {...register('email')}
            type="email"
            label="Email"
            placeholder="you@example.com"
            error={errors.email?.message}
            autoComplete="email"
            required
            disabled={isSubmitting || isLoading}
          />

          <Input
            {...register('password')}
            type="password"
            label="Password"
            placeholder="••••••••"
            error={errors.password?.message}
            autoComplete="current-password"
            required
            disabled={isSubmitting || isLoading}
          />

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full"
            isLoading={isSubmitting || isLoading}
            disabled={isSubmitting || isLoading}
          >
            Sign In
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <Link
              href="/sign-up"
              className="font-medium text-primary-600 hover:text-primary-700 transition-colors"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignInForm;
