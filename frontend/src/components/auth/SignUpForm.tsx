// T026: Sign-up form component with React Hook Form validation

'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { useAuth } from '@/hooks/useAuth';

const signUpSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      'Password must contain uppercase, lowercase, and number'
    ),
  confirmPassword: z
    .string()
    .min(1, 'Please confirm your password'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type SignUpFormData = z.infer<typeof signUpSchema>;

const SignUpForm: React.FC = () => {
  const { register: registerUser, isLoading } = useAuth();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignUpFormData>({
    resolver: zodResolver(signUpSchema),
  });

  const onSubmit = async (data: SignUpFormData) => {
    setServerError(null);

    try {
      await registerUser(data.email, data.password);
    } catch (error) {
      if (error instanceof Error) {
        setServerError(error.message);
      } else {
        setServerError('Failed to create account. Please try again.');
      }
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Create Account
          </h1>
          <p className="text-sm text-gray-600">
            Sign up to start managing your tasks
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
            helperText="Must be at least 8 characters with uppercase, lowercase, and number"
            autoComplete="new-password"
            required
            disabled={isSubmitting || isLoading}
          />

          <Input
            {...register('confirmPassword')}
            type="password"
            label="Confirm Password"
            placeholder="••••••••"
            error={errors.confirmPassword?.message}
            autoComplete="new-password"
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
            Create Account
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link
              href="/sign-in"
              className="font-medium text-primary-600 hover:text-primary-700 transition-colors"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignUpForm;
