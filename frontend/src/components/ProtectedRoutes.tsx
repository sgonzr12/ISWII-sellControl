import { Navigate, Outlet } from 'react-router-dom';

interface ProtectedRoutesProps {
  isAuthenticated: boolean;
}

function ProtectedRoutes({ isAuthenticated }: ProtectedRoutesProps) {
  if (!isAuthenticated) {
    // Redirect to the login page if not authenticated
    return <Navigate to="/" replace />;
  }
  // Render protected routes if authenticated
  return <Outlet />;
}

export default ProtectedRoutes;