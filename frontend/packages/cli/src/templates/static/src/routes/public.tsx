import { Suspense } from 'react';
import { Navigate, Outlet } from 'react-router-dom';

import { lazyImport } from '@/utils/lazyImport';
import { Loading } from 'sy-core/components/Elements';

const { AuthRoutes } = lazyImport(() => import('@/features/auth'), 'AuthRoutes');
const { Landing } = lazyImport(() => import('@/features/landing'), 'Landing');
const { About } = lazyImport(() => import('@/features/about'), 'About');

const PublicOutlet = () => {
  return (
    <Suspense fallback={<Loading load={true} />}>
      <Outlet />
    </Suspense>
  );
};

export const publicRoutes = [
  {
    path: '',
    element: <PublicOutlet />,
    children: [
      { path: '/', element: <Landing /> },
      { path: '/about', element: <About /> },
      { path: '/auth/*', element: <AuthRoutes /> },
      { path: '*', element: <Navigate to="." /> },
    ],
  },
];