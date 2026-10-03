# Assignment 3 — requirements and evidence map

Project: **Night Tokyo** — a responsive, single-page visual journal of Tokyo after dark and Japanese car culture.

This checklist is based on the supplied **Assignment 3.pdf**. Checked implementation items are supported by source review and the recorded browser results in [verification.json](verification.json). Unchecked submission items still require completion or confirmation.

## Source files

- [index.html](../index.html): sections, Bootstrap grid, navbar and components (pure HTML5).
- [style.css](../style.css): custom styling and the handmade responsive district grid.
- [DEFENSE_GUIDE.md](DEFENSE_GUIDE.md): explanations and small changes to practise before the defense.
- [verification.json](verification.json): recorded layout, asset and interaction checks.

## Recorded browser evidence

| Viewport width | Custom district columns | Bootstrap garage columns | District heading size | Horizontal overflow |
| --- | --- | --- | --- | --- |
| 375px | 1 | 1 | 44px | None detected |
| 768px | 2 | 2 | 53.6px | None detected |
| 1280px | 3 | 3 | 60.8px | None detected |

At all three widths, images and local fonts loaded, and section anchors existed. The record confirms responsive ordering, visibility and navbar behavior. Interaction checks passed for opening and closing the mobile menu, navigating to Garage, the accordion, all three garage modal stories, and dismissing a modal with Escape while restoring focus. No project console errors or failed project requests were recorded; unrelated installed-antivirus requests are listed separately in the evidence file.

Full-page evidence: [375px](screenshots/full-375.png), [768px](screenshots/full-768.png), [1280px](screenshots/full-1280.png). The 768px full-page and district captures were also independently inspected for layout and text clipping. Additional tested widths without horizontal overflow were 320px, 360px, 576px, 991px, 992px and 1440px. These results describe the recorded browser run, not every browser or device.

## Page structure and setup

| PDF requirement | Project location / evidence |
| --- | --- |
| One responsive page with at least four sections | `#home`, `#districts`, `#about`, `#garage`, `#field-notes` in `index.html` |
| Bootstrap 5.3 CSS from a CDN | Bootstrap stylesheet link in the document head |
| Custom CSS after Bootstrap CSS | `style.css` link follows the Bootstrap link |
| Viewport meta tag | `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| Bootstrap JS bundle before the closing body tag | Bundle script supports the collapsing navbar and accordion |

## Task 1 — handmade responsive section (10 points)

The **Districts** section (`#districts`) is the CSS-only example. Check the section itself and every element inside it.

- [x] Repeated district cards use the project's own CSS Grid or Flexbox rules.
- [x] There are **no Bootstrap classes** in this section, including layout, spacing, display and text utilities.
- [x] The layout uses no fixed widths or absolute positioning.
- [x] Base styles form a mobile layout with one card per row.
- [x] At least two `@media (min-width: ...)` breakpoints change the grid to two, then at least three cards per row.
- [x] At least one breakpoint also changes the heading size, spacing, alignment or image position.
- [x] At viewport widths of 375px, 768px and 1280px, the section shows one, two and at least three cards per row respectively.

For the report, include a screenshot and a short explanation of `.district-grid`: one base column, two columns from 768px, and three from 992px. At 768px, `.district-heading h2` grows from `2.75rem` to `3.35rem`, and section spacing and grid gaps change. At 992px, the heading becomes a horizontal layout and grows to `3.8rem`. The 1200px and 1400px queries only increase the maximum width of `.district-shell`.

`max-width` on `.district-shell` limits the container while allowing it to shrink; it is not a fixed `width`. The images' HTML `width` and `height` attributes describe intrinsic dimensions, while CSS uses `width: 100%` and `height: auto` for a fluid displayed size. All Districts classes, including `section-kicker`, are defined by the project.

The PDF limits Task 1 to at most half marks if the section uses desktop-first `max-width` queries or Bootstrap classes.

## Task 2 — Bootstrap layout and components (10 points)

All other main sections use Bootstrap layout. Custom visual styling is allowed; the required responsive layout should remain easy to identify in the HTML.

| Required feature | Where to demonstrate it |
| --- | --- |
| `container`, `row`, responsive `col-*` | The Bootstrap sections in `index.html` |
| Cards: one / two / at least three per row | `#garage` uses `col-12 col-md-6 col-lg-4` at 375px / 768px / 1280px |
| Two or more columns that stack on phones | Text and image in `#about` |
| Important content first on phones | `#about` text: `order-1 order-lg-2`; image: `order-2 order-lg-1` |
| Responsive visibility with `d-*` | `.mobile-note` uses `d-md-none`; the hero footer's middle label uses `d-none d-md-block` |
| Utilities such as margin, padding, flex and text | Relevant `m-*`, `p-*`, `d-flex` and `text-*` classes in the Bootstrap sections |
| Navbar that collapses on small screens | `navbar-expand-lg`, button targeting `#mainNav`, and section links |
| At least one additional Bootstrap component | Accordion `#nightNotes` in `#field-notes`, cards in `#garage`, and shared modal `#garageModal` |

- [x] No floats, fixed widths or absolute positioning are used for the layout.
- [x] No horizontal page scrolling occurs at any required width.
- [x] The navbar opens and closes on a small screen.
- [x] Navbar links reach the correct section IDs.
- [x] Accordion headers open and close their corresponding panels.
- [x] Cards, columns, text and images remain readable at all three widths.

For the report, explain the grid classes, responsive ordering, hidden or shown element, navbar and additional component. Include screenshots that make these examples readable.

## Task 3 — comparison (5 points)

Include a table with at least three rows. Compare actual parts of Night Tokyo, not only general advantages of CSS or Bootstrap.

| Aspect | Handmade CSS: Districts | Bootstrap: Garage / About |
| --- | --- | --- |
| Where the column rules live | `style.css` contains the grid and explicit media queries | Responsive column classes are written on elements in `index.html` |
| Changing the laptop card count | Edit the wider grid rule in `style.css` | Change the garage cards' large-screen column class |
| Control and reusable behavior | The district layout and its heading/spacing changes are defined directly | Grid, ordering and visibility behavior come from Bootstrap classes; custom CSS supplies the visual design |
| Components | A custom card layout needs only the project's CSS | Navbar collapse and accordion use Bootstrap's bundle and attributes |

Suggested choice explanation to rewrite in your own words: “I would use custom CSS when a section needs a specific layout or coordinated changes to its typography and spacing. I would use Bootstrap when I need common responsive columns, ordering and interactive components quickly. This page uses both so the district grid can be tailored while the other sections share Bootstrap's layout system.”

## Report and submission (5 points)

The final report must be named **`Assignment3_YourName.docx`** or **`Assignment3_YourName.pdf`**, with `YourName` replaced by your name. The PDF states that other submission formats receive zero. Markdown files are supporting notes and do not replace the required report.

Use this report order:

1. Student name, group and project title.
2. Task 1: screenshots and a short explanation in your own words.
3. Task 2: screenshots and a short explanation in your own words.
4. Task 3: comparison table and two or three sentences explaining when to choose each method.
5. Readable **whole-page screenshots at viewport widths 375px, 768px and 1280px**. Label the width of each image; add detail screenshots if needed for readability.
6. A short conclusion about what you learned.
7. The actual GitHub repository URL containing all source code.

- [x] Capture the complete page at 375px, 768px and 1280px, with supporting section and interaction screenshots.
- [ ] Replace every student-name, group and repository placeholder.
- [ ] Confirm the report file opens correctly and screenshots are readable.
- [ ] Upload the final source files and required local assets to GitHub.
- [ ] Check that the repository URL in the report opens the correct repository.
- [ ] Submit before the course deadline and attend the practical defense.

The assignment is individual. The supplied PDF states that identical work, missing the repository link, submitting late, missing the defense, or being unable to explain the code can result in zero. No submission deadline date is provided in the supplied PDF; check the course system.

## Defense (70 points)

- 10 points: explain the work and demonstrate the page live without errors.
- 30 points: answer questions about the code and the topic.
- 30 points: make the instructor's requested change without assistance or hints.

Use the [defense guide](DEFENSE_GUIDE.md) to prepare. Understanding and practising the changes is part of completing the assignment.
