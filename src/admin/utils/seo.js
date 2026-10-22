/**
 * SEO helpers for the admin dashboard (/admin/*).
 * The dashboard must never be indexed, and the customer site's
 * title/description are restored when leaving /admin.
 */

const ADMIN_TITLE = 'TicketsAnywhere Admin Dashboard';
const ADMIN_DESCRIPTION = 'Manage events, view sales analytics, handle orders and customer data.';

const upsertMeta = (name, content) => {
  let tag = document.querySelector(`meta[name="${name}"]`);
  if (!tag) {
    tag = document.createElement('meta');
    tag.name = name;
    document.head.appendChild(tag);
  }
  const previous = tag.getAttribute('content');
  tag.setAttribute('content', content);
  return { tag, previous };
};

export const updateAdminMetaTags = ({
  title = ADMIN_TITLE,
  description = ADMIN_DESCRIPTION,
} = {}) => {
  document.title = title;
  upsertMeta('description', description);
};

/**
 * Applies admin meta tags (title, description, robots=noindex) and returns a
 * cleanup function that restores the previous values.
 */
export const applyAdminMetaTags = () => {
  const previousTitle = document.title;
  const description = upsertMeta('description', ADMIN_DESCRIPTION);
  const robots = upsertMeta('robots', 'noindex, nofollow');
  document.title = ADMIN_TITLE;

  return () => {
    document.title = previousTitle;
    if (description.previous === null) description.tag.remove();
    else description.tag.setAttribute('content', description.previous);
    if (robots.previous === null) robots.tag.remove();
    else robots.tag.setAttribute('content', robots.previous);
  };
};

export const resetAdminMetaTags = () => updateAdminMetaTags();
