const path = require('path');
const fs = require('fs');
const pug = require('pug');

const args = process.argv.slice(2);
const html = pug.renderFile('src/index.pug')

if (args.includes('-all')) {
    args.push('-html', '-css');
}

if (args.includes('-html')) {
    fs.writeFile('build/index.html', html, () => {});
}

if (args.includes('-css')) {
    const PurgeCSS = require('purgecss').default;
    new PurgeCSS().purge({
        content: [
            {raw: html, extension: 'html'},
            'src/scripts.js',
            'src/assets/mail/contact_me.js',
            'src/assets/mail/jqBootstrapValidation.js',
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
}
