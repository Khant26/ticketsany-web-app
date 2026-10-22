import { lazy, Suspense } from "react";
import { Navigate } from "react-router";
import AdminRoot from "./AdminRoot";

// Admin pages are lazy-loaded so the customer bundle does not include them.
const AdminAuthGuard = lazy(() => import("./components/AdminAuthGuard"));
const AdminLayout = lazy(() => import("./components/AdminLayout"));
const AdminLogin = lazy(() => import("./pages/AdminLogin"));
const AdminHome = lazy(() => import("./pages/AdminHome"));
const EventUpload = lazy(() => import("./pages/EventUpload"));
const StatusChange = lazy(() => import("./pages/StatusChange"));
const UploadBanner = lazy(() => import("./pages/UploadBanner"));
const CategoriesManagement = lazy(() => import("./pages/CategoriesManagement"));
const EditEvent = lazy(() => import("./pages/EditEvent"));
const AdminProfile = lazy(() => import("./pages/AdminProfile"));
const AddNewEvents = lazy(() => import("./pages/AddNewEvents"));
const AllTickets = lazy(() => import("./pages/AllTickets"));

const AdminLoading = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
  </div>
);

const withSuspense = (element) => (
  <Suspense fallback={<AdminLoading />}>{element}</Suspense>
);

const ProtectedAdminLayout = () =>
  withSuspense(
    <AdminAuthGuard>
      <AdminLayout />
    </AdminAuthGuard>
  );

const page = (Component) => () => withSuspense(<Component />);

const adminRoutes = [
  {
    path: "/admin",
    Component: AdminRoot,
    children: [
      { path: "login", Component: page(AdminLogin) },
      {
        Component: ProtectedAdminLayout,
        children: [
          { index: true, Component: page(AdminHome) },
          { path: "eventupload", Component: page(EventUpload) },
          { path: "statuschange", Component: page(StatusChange) },
          { path: "uploadbanner", Component: page(UploadBanner) },
          { path: "categories", Component: page(CategoriesManagement) },
          { path: "events/:id/edit", Component: page(EditEvent) },
          { path: "adminProfile", Component: page(AdminProfile) },
          { path: "addNewEvents", Component: page(AddNewEvents) },
          { path: "alltickets", Component: page(AllTickets) },
          { path: "*", Component: () => <Navigate to="/admin" replace /> },
        ],
      },
    ],
  },
];

export default adminRoutes;
