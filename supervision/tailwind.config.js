/** @type {import('tailwindcss').Config} */
module.exports = {
        content: [
            './templates/**/*.html',
            './node_modules/flowbite/**/*.js'
        ],
        theme: {
          extend: {
                fontFamily: {
                        mona: ["Mona Sans", "sans"],
                        monaebold: ["Mona Sans Ebold", "sans"],
                        monamn: ["Mona Sans Medium Narrow", "sans"]
                }
          },
        },
        plugins: [require('flowbite/plugin')],
}
