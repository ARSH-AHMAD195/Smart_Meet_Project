import { Navigate, useNavigate } from "react-router";
import { useEffect, useState } from "react";
import api from "../api/backend_api";

function ProtectedRoute({ children }) {
  const navigate = useNavigate();
  const [valid, setValid] = useState(null); // null = checking

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setValid(false);
      return;
    }

    api.get("/auth/verify-token")
      .then(() => setValid(true))
      .catch(() => {
        localStorage.removeItem("access_token");
        setValid(false);
      });
  }, []);

  if (valid === null) {
    return (
      <div className="w-full h-screen flex justify-center items-center text-white">
        Checking Authentication...
      </div>
    );
  }

  return valid ? children : <Navigate to="/signin" />;
}

export default ProtectedRoute;
