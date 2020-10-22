const path = require('path');
const pug = require('pug');
const fs = require('fs');

const PurgeCSS = require('purgecss').default;

const html = pug.renderFile('src/index.pug')
fs.writeFile('build/index.html', html, () => {});


new PurgeCSS().purge({
    content: [
        {raw: html, extension: 'html'},
        'src/scripts.js',
        'node_modules/bootstrap/dist/js/bootstrap.min.js'
    ],
    css: ['src/styles.css']
}).then(
    css => css.map(
        file => fs.writeFile(
            file.file.replace('src', 'build'),
            file.css,
            () => {}
        )
    )
);