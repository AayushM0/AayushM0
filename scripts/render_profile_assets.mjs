import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const assets = new URL('../assets/', import.meta.url);
const glyphs = {
  A: ['01110','10001','10001','11111','10001','10001','10001'],
  Y: ['10001','10001','01010','00100','00100','00100','00100'],
  U: ['10001','10001','10001','10001','10001','10001','01110'],
  S: ['01111','10000','10000','01110','00001','00001','11110'],
  H: ['10001','10001','10001','11111','10001','10001','10001'],
  M: ['10001','11011','10101','10101','10001','10001','10001'],
  I: ['11111','00100','00100','00100','00100','00100','11111'],
  T: ['11111','00100','00100','00100','00100','00100','00100'],
  L: ['10000','10000','10000','10000','10000','10000','11111'],
};
const rows = Array.from({ length: 7 }, (_, row) =>
  [...'AAYUSH MITTAL'].map(letter => letter === ' ' ? '000' : glyphs[letter][row]).join('0'));
const cols = rows[0].length + 4;
const palette = ['#0e4429', '#006d32', '#26a641', '#39d353'];
let cells = '';
for (let row = 0; row < 11; row++) {
  for (let col = 0; col < cols; col++) {
    const lit = row >= 2 && row < 9 && rows[row - 2][col - 2] === '1';
    const noise = (col * 17 + row * 31) % 37 === 0;
    const color = lit ? palette[2 + ((col + row) % 3 === 0 ? 0 : 1)]
      : noise ? palette[(col + row) % 2] : '#161b22';
    cells += `<rect x="${24 + col * 13}" y="${59 + row * 13}" width="10" height="10" rx="1.5" fill="${color}"/>`;
  }
}
const width = cols * 13 + 45;
writeFileSync(new URL('name-heatmap.svg', assets), `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="244" viewBox="0 0 ${width} 244" role="img" aria-labelledby="title desc">
<title id="title">Aayush Mittal</title><desc id="desc">Aayush Mittal spelled in green GitHub contribution-style squares.</desc>
<rect width="${width}" height="244" rx="12" fill="#0d1117"/>
<g font-family="monospace" font-size="11" fill="#8b949e"><text x="24" y="30">AAYUSHM0 / OPEN SOURCE &amp; EXPERIMENTS</text><text x="${width - 24}" y="30" text-anchor="end" fill="#39d353">● BUILDING, ONE COMMIT AT A TIME</text></g>
${cells}
<text x="24" y="225" font-family="monospace" font-size="11" fill="#8b949e">FULL-STACK ENGINEERING · AGENTIC AI · DEVELOPER TOOLING</text>
</svg>\n`);

const cards = [
  ['link-portfolio.svg', '01 / EXPLORE', 'Selected work', 'aayushmittal.me', '<path d="M8 15l-5 5 5 5m24-10l5 5-5 5M24 9l-8 22"/>'],
  ['link-resume.svg', '02 / BACKGROUND', 'The story so far', 'Read my résumé', '<path d="M10 4h14l8 8v24H10zM24 4v9h8M16 20h10M16 26h10"/>'],
  ['link-email.svg', '03 / SAY HELLO', 'Let’s build something', 'aayushmittal620@gmail.com', '<rect x="3" y="8" width="34" height="25" rx="3"/><path d="M4 10l16 13 16-13"/>'],
];
for (const [file, eyebrow, label, detail, icon] of cards) {
  writeFileSync(new URL(file, assets), `<svg xmlns="http://www.w3.org/2000/svg" width="480" height="104" viewBox="0 0 480 104" role="img" aria-labelledby="title">
<title id="title">${label} — ${detail}</title>
<rect x=".5" y=".5" width="479" height="103" rx="10" fill="#0d1117" stroke="#30363d"/>
<rect x="1" y="24" width="3" height="56" rx="1.5" fill="#39d353"/>
<g transform="translate(20 32)" fill="none" stroke="#39d353" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${icon}</g>
<text x="80" y="25" font-family="monospace" font-size="10" letter-spacing="1.4" fill="#39d353">${eyebrow}</text>
<text x="80" y="53" font-family="system-ui, sans-serif" font-size="20" font-weight="600" fill="#e6edf3">${label}</text>
<text x="80" y="78" font-family="monospace" font-size="12" fill="#8b949e">${detail}</text>
<path d="M437 43h15v15m-15 0l15-15" fill="none" stroke="#39d353" stroke-width="1.8"/>
</svg>\n`);
}
console.log(`Generated name banner and three link cards in ${fileURLToPath(assets)}`);
