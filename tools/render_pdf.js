// Print the PDF edition of the notes with headless Chromium.
//   node tools/render_pdf.js print.html out.pdf
// Called by `python3 build.py --pdf` (which writes print.html and adds bookmarks afterwards).
// Needs the `playwright` npm package and its Chromium. MathJax comes from the CDN unless MATHJAX_JS
// points to a local copy of mathjax@3/es5/tex-svg.js (or `mathjax` is installed next to this script).
const { chromium } = require('playwright');
const path = require('path');

function localMathJax() {
  if (process.env.MATHJAX_JS) return path.resolve(process.env.MATHJAX_JS);
  try { return require.resolve('mathjax/es5/tex-svg.js'); } catch (e) { return null; }
}

(async () => {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) throw new Error('usage: node tools/render_pdf.js print.html out.pdf');
  const browser = await chromium.launch();
  // 180 mm (A4 minus the side margins) at 96 px per inch, so scripts lay out at the printed width
  const page = await browser.newPage({ viewport: { width: 680, height: 1000 } });
  const problems = [];
  page.on('pageerror', e => problems.push('page error: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') problems.push('console: ' + m.text()); });
  const mj = localMathJax();
  if (mj) await page.route(/mathjax.*tex-svg\.js/, r => r.fulfill({ path: mj, contentType: 'application/javascript' }));

  await page.goto('file://' + path.resolve(input), { waitUntil: 'load', timeout: 180000 });
  await page.waitForFunction(() => document.documentElement.dataset.mj, null, { timeout: 900000, polling: 500 });
  const state = await page.evaluate(() => document.documentElement.dataset.mj);
  if (state !== 'done') throw new Error('MathJax did not finish: ' + state);
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });

  const report = await page.evaluate(() => {
    const q = s => Array.from(document.querySelectorAll(s));
    return {
      mathErrors: q('mjx-merror, [data-mjx-error]').length,
      unrendered: (document.getElementById('main').innerText.match(/\\\(|\\\[/g) || []).length,
      plotErrors: q('figure.plot, .widget').filter(f => /error/i.test(f.textContent.slice(0, 80))).length,
      wideTables: q('.tbl').filter(t => t.scrollWidth > t.clientWidth + 2).length,
    };
  });
  for (const [k, v] of Object.entries(report)) if (v) problems.push(k + ': ' + v);

  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true });
  await browser.close();
  if (problems.length) { console.error(problems.join('\n')); process.exitCode = 2; }
})().catch(e => { console.error(e); process.exit(1); });
