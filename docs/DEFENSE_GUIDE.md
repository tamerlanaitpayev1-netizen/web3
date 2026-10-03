# Night Tokyo — defense guide

Use this as a study guide. Read the actual code, explain it in your own words, and practise changes yourself. Recorded browser results are in [verification.json](verification.json); the exercises below are preparation for your own defense.

## A short introduction

“My project is Night Tokyo, a responsive single-page website about Tokyo at night. It has five main sections: Home, Districts, About, Garage and Field Notes. I made the Districts section responsive with my own CSS Grid and media queries. I used Bootstrap for the other sections, including responsive columns, the navigation menu and the accordion.”

Open these files while preparing:

- [index.html](../index.html): structure, Bootstrap classes, data-attributes, and native modals.
- [style.css](../style.css): typography, theme tokens, and the handmade CSS Grid responsive section.
- [REQUIREMENTS.md](REQUIREMENTS.md): the assignment checklist and report requirements.

## Explain the handmade section

Find `id="districts"` in `index.html`, then find `.district-grid` in `style.css`.

“The base layout has one column, so it works on a narrow phone screen first. A `min-width` media query adds two columns when the viewport is wide enough. A second media query adds three columns on larger screens. I also change the heading size or spacing at a breakpoint, so the responsive changes affect more than the number of columns.”

The important pattern is:

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

These are the project's grid selectors and column breakpoints; the full rules also contain spacing changes. At 768px, `.district-heading h2` grows from `2.75rem` to `3.35rem`. At 992px, it grows to `3.8rem` and `.district-heading` changes from a vertical to a horizontal layout. The additional 1200px and 1400px queries widen the container without changing the three-column grid.

- `display: grid` turns the element into a grid container.
- `repeat(3, ...)` creates three equal tracks.
- `1fr` means one equal share of the available space.
- `minmax(0, 1fr)` allows a track to shrink without its content's default minimum width forcing it wider.
- `gap` adds space between cards without adding space outside the grid.
- `min-width: 768px` means that the rule applies at **768px and wider**, not only at exactly 768px.
- At a larger width, multiple `min-width` queries can apply. Later rules with equal specificity can override earlier rules.

Bootstrap CSS is loaded on the page, but this section uses no Bootstrap classes. Its responsive layout comes from the project's own CSS. `section-kicker` is a custom class in `style.css`, even though other sections also reuse it.

`.district-shell` uses `max-width` to cap the content width on large screens. It can still shrink, unlike a fixed `width`. Image `width` and `height` attributes provide intrinsic dimensions; CSS `width: 100%` and `height: auto` make the displayed images responsive.

## Explain the Bootstrap sections

Find the card columns in `#garage` in `index.html`. Each uses this pattern:

```html
<div class="col-12 col-md-6 col-lg-4">
  <!-- A card -->
</div>
```

“Bootstrap divides a row into 12 columns. `col-12` uses the whole row, so there is one card per row on a phone. At the `md` breakpoint, `col-md-6` uses six of the 12 columns, so two cards fit. At the `lg` breakpoint, `col-lg-4` uses four columns, so three cards fit.”

| Class / breakpoint | Meaning |
| --- | --- |
| `container` | Centers the content and provides responsive container sizing and horizontal padding |
| `row` | Holds columns and works with the grid's gutters |
| `col-12` | Full row width at the base size |
| `md` | Applies from 768px |
| `lg` | Applies from 992px |
| `g-*` | Sets grid gutters |
| `p-*`, `m-*` | Set padding and margin using Bootstrap's spacing scale |
| `d-flex` | Uses Flexbox for that element |
| `text-*` | Text utilities; the exact suffix determines the behavior |

Bootstrap classes also work mobile-first. A breakpoint class continues to apply above its breakpoint until another applicable rule overrides it.

### Stacking and ordering

Show the image and text columns in `#about`.

“The columns use the full row width on a phone, so the content stacks vertically. The more important text appears first. At a wider breakpoint, the columns sit beside each other. `order-*` classes can change their visual order at a particular width.”

The text uses `order-1 order-lg-2`; the image uses `order-2 order-lg-1`. Text has order 1 below 992px and order 2 from 992px. The image has the reverse values, so the two swap visually. CSS order changes the visual arrangement; it does not change the HTML or reading order in the document. The text already comes first in the HTML.

### Responsive visibility

Show these two elements in `#home`:

- The middle label in `.hero-footer` uses `d-none d-md-block`: hidden below 768px, displayed as a block from 768px.
- The paragraph `.mobile-note` uses `d-md-none`: hidden from 768px; below that, it keeps its normal paragraph display.

“I use responsive visibility for secondary content so that the mobile layout stays readable.”

### Navbar and accordion

“The navbar links use section IDs, such as `href="#districts"`. `navbar-expand-lg` expands the menu at 992px; below that, the links are behind a menu button. The button targets `#mainNav`. Bootstrap's bundle handles the button and the accordion. The `data-bs-target` or `href` target must match the ID of the element that should open.”

For an accordion, each button must target the correct panel ID. `aria-expanded` communicates whether a panel is open, and `aria-controls` identifies the controlled panel. Follow the existing markup when adding another item, and use unique IDs.

### Why the project uses pure HTML/CSS without custom JavaScript

“The assignment is dedicated to CSS media queries and the Bootstrap responsive grid. In strict compliance with the requirements, I did not write custom JavaScript. All interactive features—the collapsible navigation menu, the expandable field-notes accordion, and the garage modals—are driven by native Bootstrap 5.3 data-attributes (`data-bs-toggle`, `data-bs-target`, `data-bs-dismiss`) and the official Bootstrap CDN bundle.

Each car in the garage targets its own dedicated static modal (`#garageModalSkyline`, `#garageModalSupra`, `#garageModalRx7`) with full semantic content. This approach guarantees zero JavaScript console errors, complete accessibility, and clean separation of concerns.”

## Questions you should be able to answer

**What does responsive mean?**  
The layout adapts to the available viewport width while keeping content usable and readable.

**What is the viewport?**  
It is the area in which the browser lays out the page. The required 375px, 768px and 1280px measurements are viewport widths in CSS pixels.

**Why is the viewport meta tag necessary?**  
`width=device-width` makes the mobile layout viewport follow the device width, and `initial-scale=1` sets the initial zoom scale. Without it, a phone may use a wider virtual layout viewport and shrink the page, so the intended mobile layout does not appear.

**Why is this mobile-first?**  
The unqualified CSS defines the phone layout. Increasing `min-width` queries add changes for larger screens.

**Why does `style.css` load after Bootstrap?**  
For rules with the same cascade priority and specificity, later rules win. Loading custom CSS later helps override Bootstrap defaults, although specificity and other cascade rules still matter.

**Are CSS media queries and Bootstrap unrelated?**  
No. Bootstrap's responsive grid also uses CSS and media queries. The difference is whether I write the responsive rules myself or use predefined classes.

**When would you choose each method?**  
I would choose custom CSS for a layout that needs exact control over its structure, typography and spacing. I would choose Bootstrap for common responsive grids and components that can share established patterns.

## Practise live changes

1. **Change the handmade laptop grid from three to four columns.** Find the 992px media query for `.district-grid` in `style.css`. Change `repeat(3, minmax(0, 1fr))` to `repeat(4, minmax(0, 1fr))`. There are currently three district cards, so add a fourth article if the instructor asks to see four actual cards in the row. Check that the phone and tablet rules still work.
2. **Change the Bootstrap laptop cards from three to four per row.** In `index.html`, change the garage columns from `col-lg-4` to `col-lg-3`. Four columns fit because `12 / 3 = 4`. Apply the change consistently to every garage card column. Add a fourth column and card if a complete row of four is requested; update its story data if it needs its own modal text.
3. **Move the handmade tablet breakpoint.** Change its `min-width` value, then resize just below and at the new value. Keep the assignment's required two-card result at 768px for the submitted version.
4. **Adjust the heading at a breakpoint.** Find the district heading rule inside a media query and change its `font-size`. The base phone heading should still use the base rule.
5. **Swap text and image on wide screens.** Edit the large-screen `order-*` classes on both About columns. Keep the important text first on phones.
6. **Show a secondary element only on phones.** Use a suitable base display and `d-md-none` in a Bootstrap section. Do not add Bootstrap classes to Districts.
7. **Add an accordion item.** Copy an existing item's structure, replace its text, and give the heading, button target and panel matching unique IDs.

Return practice changes to the intended final version before submitting.

## Live demonstration checklist

These are checks to perform, not recorded test results.

1. Open the page with an internet connection for Bootstrap's CDN resources, or use locally downloaded Bootstrap files if the project has been adapted for offline use.
2. Set the browser's responsive viewport to **375px**. Show the single-column district and garage layouts, the stacked About content, and the mobile menu.
3. At **768px**, show the two-card layouts and explain which rules apply.
4. At **1280px**, show the larger grids and the side-by-side content.
5. Open and close the navbar and accordion; follow the section links.
6. Look for horizontal overflow, unreadable text, cropped content and broken images. Check the browser console for errors.
7. Show the relevant CSS and HTML, then make one of the practice changes without reading the answer.

The defense is worth **70 of 100 points**: 10 for explanation and demonstration, 30 for questions, and 30 for an independent live change.
