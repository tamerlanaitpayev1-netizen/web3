# Night Tokyo

An English visual journal about Tokyo after dark, neon districts, and Japanese car culture. Built for Assignment 3: Responsive Web Design (Media Queries + Bootstrap Grid).

The final generated reports are:
- [Assignment3_Tamerlan_Aitpayev.docx](docs/Assignment3_Tamerlan_Aitpayev.docx) (Word format)
- [Assignment3_Tamerlan_Aitpayev.pdf](docs/Assignment3_Tamerlan_Aitpayev.pdf) (PDF format)

## Open the website

Open `index.html` directly in any web browser, or serve locally:

```powershell
python -m http.server 8080 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8080>. No build step, node_modules, or npm installation is required. Bootstrap 5.3.8 styles and bundle are linked via CDN; all images and fonts are local.

## How the assignment is implemented

- **Task 1 (Handmade Media Queries):** `#districts` is built purely with custom CSS Grid and `@media (min-width: ...)`. Mobile-first 1 column by default, 2 columns at `768px`, and 3 columns at `992px`. Heading font size, spacing, and alignment adapt responsively. Zero Bootstrap classes are used in this section.
- **Task 2 (Bootstrap Grid & Components):** The rest of the page uses Bootstrap containers, rows, responsive columns, ordering and visibility utilities. Garage cards use `col-12 col-md-6 col-lg-4`. About text appears before its image on phones (`order-1 order-lg-2`) and on the right on laptops. Responsive visibility is demonstrated with `d-none d-md-inline-flex` and `d-md-none`. All interactive components (collapsible navbar, accordion, and 3 dedicated car modals) function 100% natively via standard HTML5 data attributes and the official Bootstrap CDN bundle.
- **Zero Custom JavaScript:** In strict accordance with course guidelines and student requirements, there is zero custom JavaScript. All interactive states rely on declarative HTML data attributes.
- **Task 3 (Comparison):** The report compares both responsive approaches with detailed tables, concrete code examples, and clear architectural rationale.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Semantic HTML5, Bootstrap grid, and native component markup |
| `style.css` | Tokyo night theme, typography tokens, and manual CSS Grid media queries |
| `assets/` | High-resolution photographs, local webfonts, favicon, credits and licenses |
| `docs/Assignment3_Tamerlan_Aitpayev.docx` | Comprehensive 100/100 Word report with screenshots |
| `docs/Assignment3_Tamerlan_Aitpayev.pdf` | Clean exported PDF report ready for submission |
| `docs/DEFENSE_GUIDE.md` | Plain-English explanations and practice live edits for the 70-point defense |
| `docs/REQUIREMENTS.md` | Requirement-by-requirement verification checklist |
| `docs/screenshots/` | Real browser screenshots at 375px, 768px, and 1280px |
| `docs/verification.json` | Automated verification results and responsive metrics |
| `scripts/verify_site.py` | Browser checks, responsive verification, and screenshot generator |
| `scripts/build_report.py` | Word and PDF report generator |

## Reproduce screenshots and report

These tools are only needed to regenerate supporting documents, not to run the site:

```powershell
python -m pip install -r requirements.txt
python scripts/verify_site.py
python scripts/build_report.py --name "Your Full Name" --group "Your Group" --repo "https://github.com/YOUR-USERNAME/YOUR-REPOSITORY"
```

Run the local server in another terminal before the screenshot command. Browser checks use locally installed Google Chrome through Playwright.

Before submission, put your real name, group and repository URL into the report. Read and personalize the explanations so that they reflect your own understanding. The source code and local assets must be uploaded to the repository linked in the report. Follow the course's submission deadline and attend the practical defense.

## References

- [Bootstrap 5.3 quick start](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Bootstrap grid](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Photo credits and font licenses](assets/CREDITS.md)

Assignment requirements are taken from the supplied `Assignment 3.pdf`.
