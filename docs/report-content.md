# Assignment 3 — Night Tokyo

This is an editable English preview of the report explanations. The document generator contains the equivalent text and combines it with real browser screenshots and recorded verification results. Edit the generated DOCX directly to personalize the final report; changes to this preview do not automatically change the generator. Before submission, add your full name, group, and the URL of the GitHub repository containing the source code. Review the explanation and put it in your own words so that you can explain it during the defense.

- Student: **Tamerlan Aitpayev**
- Group: **SE-2401**
- GitHub repository: **https://github.com/TamerlanAitpayev/web3**
- Report filename: **Assignment3_Tamerlan_Aitpayev.docx** (and **.pdf**)

## Project overview and setup

Night Tokyo is an English-language editorial website about Tokyo at night, its districts, and Japanese car culture. Its browser title is “Night Tokyo — The city comes alive after dark.” It has five content sections: the opening hero (`#home`), district cards (`#districts`), an editorial story (`#about`), a garage of car cards (`#garage`), and expandable field notes (`#field-notes`).

Bootstrap 5.3.8 is connected through its CDN. The custom `style.css` is loaded after Bootstrap, so the page can override the default appearance. The Bootstrap JavaScript bundle is loaded before the closing body tag for the navigation menu, accordion, and modals. The page includes `<meta name="viewport" content="width=device-width, initial-scale=1">`, which makes the responsive layout use the device's actual viewport width. The project strictly requires **zero custom JavaScript**, relying purely on semantic HTML5, CSS3, and standard Bootstrap data attributes.

## Task 1 — Media queries by hand

The districts are built with custom CSS only. Their base grid contains one flexible column. A `min-width: 768px` media query creates two columns; a `min-width: 992px` query creates three. The tablet breakpoint also changes the section spacing and heading size. All classes inside this section are custom classes, and its layout does not use Bootstrap columns, fixed card widths, floats, or absolute positioning.

The layout pattern is:

```css
.district-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
}

@media (min-width: 768px) {
  .district-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 992px) {
  .district-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
```

This is a short layout excerpt; `style.css` contains the complete rules. At 375px, only the base rule applies. At 768px, the first query applies. At 1280px, both queries apply and the later rule makes three columns. `minmax(0, 1fr)` lets the tracks shrink when needed, helping prevent content from forcing horizontal overflow.

Screenshot evidence: `districts-375.png`, `districts-768.png`, and `districts-1280.png` in `docs/screenshots/`.

## Task 2 — Bootstrap grid and components

The other sections use Bootstrap containers, rows, and responsive columns. Every garage card wrapper has `col-12 col-md-6 col-lg-4`. The columns therefore occupy the full row on phones, half the row from 768px, and one third of the row from 992px.

The story section contains text and an image. The text is the first item in the HTML and uses `order-1 order-lg-2`; the image uses the opposite order. On a phone, the reader sees the important text first and the image underneath. On a large screen, the columns sit next to each other and the image appears on the left.

The status label uses `d-none d-md-inline-flex`, which hides it below 768px. A phone hint uses `d-md-none`, which hides it at 768px and above. Bootstrap spacing, flex, and text utilities handle recurring spacing and alignment.

The `navbar-expand-lg` navigation becomes a menu button below 992px. Its links point to the section IDs on the same page. The Bootstrap JavaScript bundle controls the collapse behavior and the field-notes accordion. Bootstrap cards provide the repeated garage component. Their buttons open dedicated Bootstrap modals (`#garageModalSkyline`, `#garageModalSupra`, `#garageModalRx7`) with short editorials about each car. All interactive components work declaratively via Bootstrap's built-in `data-bs-*` attributes with zero custom JavaScript.

Screenshot evidence: the three `garage-*.png` captures, `about-mobile.png`, `about-desktop.png`, `navbar-mobile.png`, `accordion-open.png`, and `garage-modal.png`.

## Task 3 — Comparison

| Aspect | Custom district grid | Bootstrap garage / other sections |
| --- | --- | --- |
| Layout code | A base grid rule and two `min-width` queries in `style.css`. | `col-12 col-md-6 col-lg-4` on each card wrapper; Bootstrap supplies the breakpoint rules. |
| Design control | A section-specific query can change the grid, heading, and spacing together. | Bootstrap handles columns and gutters; custom CSS adds the night-Tokyo appearance. |
| Making changes | Edit `grid-template-columns` in the 992px query to change the laptop card count. | Use `col-lg-3` for a four-card desktop row. |
| Speed and reuse | Write and maintain the small repeated layout's CSS directly. | Reuse column patterns and the existing navbar and accordion behavior. |
| Ordering / visibility | Requires extra custom `order` and `display` rules. | Use `order-*` and `d-*` utilities, as in the story and status label. |

I would choose custom media queries for a distinctive section such as the districts, where the spacing and heading need to change together with the card layout. I would choose Bootstrap for repeated card layouts and page structure, especially when the page also needs a responsive navbar or accordion. Combining both approaches keeps the district design flexible while making the rest of this page quicker to maintain.

## Conclusion

I learned how to build a mobile-first layout with both CSS Grid media queries and Bootstrap's responsive columns. I learned how breakpoints produce one, two, and three cards per row, and how ordering and display utilities help prioritize content on smaller screens. I also learned why checking several viewport widths matters: a layout can look correct on a laptop and still overflow or become difficult to read on a phone.

## Verification and complete-page evidence

The generator reads `docs/verification.json` when it exists and presents its actual recorded responsive-layout metrics and interaction results in readable tables. The original JSON remains available for the complete results. If that file is absent, the report explicitly says that no automated verification record was available. Screenshots alone are not treated as proof that all interaction checks passed.

The complete page screenshots are `full-375.png`, `full-768.png`, and `full-1280.png`. The report splits tall captures into consecutive, labeled panels for readability without omitting any content. Original images remain available for inspection.

## Technical references

- [Bootstrap introduction](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Bootstrap grid](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Bootstrap display utilities](https://getbootstrap.com/docs/5.3/utilities/display/)
- [Bootstrap navbar](https://getbootstrap.com/docs/5.3/components/navbar/)
- [Bootstrap accordion](https://getbootstrap.com/docs/5.3/components/accordion/)
- [MDN: Using media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries)

## Building the DOCX

After the screenshots have been captured, run:

```powershell
python scripts/build_report.py --name "First Last" --group "SE-2401" --repo "https://github.com/USERNAME/REPOSITORY"
```

The default output is `docs/Assignment3_First_Last.docx`. If personal details are not supplied, it creates `docs/Assignment3_YourName.docx` with explicit placeholders. A missing screenshot prevents a normal build; use `--draft` only for a visibly incomplete preview.
