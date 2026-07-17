# Personal website

A small, static personal website — plain HTML and one CSS file, no build step.
Designed to grow over time.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Home page with a short intro |
| `about.html` | About me |
| `research.html` | Research focus and peer-reviewed publications |
| `teaching.html` | University teaching (e-business, internet economics) |
| `services.html` | Data science & consulting services |
| `blog.html` | Blog index |
| `posts/` | Individual blog posts |
| `contact.html` | Contact details |
| `impressum.html` | Legal notice (Impressum, German) |
| `datenschutz.html` | Privacy policy (Datenschutz, German) |
| `404.html` | Shown for unknown URLs |
| `style.css` | Shared styling for every page |
| `favicon.svg` | Browser-tab icon (RT monogram) |
| `images/` | Site images — e.g. `rene-theuerkauf.jpg` portrait |

> **Before publishing:** the legal pages (`impressum.html`, `datenschutz.html`)
> are filled in (address, IONOS hosting) but remain templates — have them checked
> and add a VAT ID in the Impressum if you have one.

## Editing

- Text lives directly in the `.html` files. Look for the `<!-- comments -->`
  marking the parts to replace, and the italic "placeholder" boxes.
- To change colours or fonts site-wide, edit the variables at the top of
  `style.css` (the `:root { … }` block).
- The navigation menu is repeated in each file's `<header>`. If you add a new
  page, copy an existing one and add a matching link to every menu.

## Preview locally

Just double-click `index.html` to open it in your browser. For a more accurate
local server (optional), run this in the folder and visit http://localhost:8000:

```
python -m http.server 8000
```

## Publishing on GitHub Pages

> Note: with a **free** GitHub account, a custom domain requires the repository
> to be **public**. (The source files are visible, but that's normal for a
> static site.)

1. Create a GitHub account if you don't have one.
2. Create a new **public** repository. For a site at `https://<username>.github.io`,
   name it exactly `<username>.github.io`. Any other name gives you a project
   site at `https://<username>.github.io/<repo>/` — both work with a custom
   domain.
3. Upload all the files in this folder to the repository (drag-and-drop in the
   browser works, or use `git`).
4. In the repo: **Settings → Pages**. Under "Build and deployment", set
   **Source = Deploy from a branch**, **Branch = main**, **Folder = / (root)**,
   then **Save**.
5. Wait a minute, then visit the URL GitHub shows on that page.

## Connecting your domain (when you're ready)

1. In **Settings → Pages → Custom domain**, type your domain (e.g.
   `example.com`) and **Save**. GitHub creates a `CNAME` file in the repo.
2. At your domain registrar's DNS settings, add records:
   - For an **apex** domain (`example.com`) add four **A** records pointing to:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     (and optionally the matching AAAA records for IPv6).
   - For a **www** subdomain (`www.example.com`) add a **CNAME** record pointing
     to `<username>.github.io`.
3. Back in **Settings → Pages**, wait for the check to pass, then tick
   **Enforce HTTPS**.

DNS changes can take anywhere from a few minutes to a day to take effect.

## Notes

- The `style.css` link in `index.html` and the subpages uses a relative path,
  which works both locally and on GitHub Pages. `404.html` uses absolute paths
  (`/style.css`) because GitHub serves it from any URL.
