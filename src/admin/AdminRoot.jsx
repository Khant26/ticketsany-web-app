import { useEffect } from "react";
import { Outlet } from "react-router";
import { applyAdminMetaTags } from "./utils/seo";

// Top-level wrapper for every /admin/* route. Sets admin-only meta tags
// (noindex) and scopes admin markup under `.admin-app`.
function AdminRoot() {
  useEffect(() => applyAdminMetaTags(), []);

  return (
    <div className="admin-app">
      <Outlet />
    </div>
  );
}

export default AdminRoot;
