drafts for codey blog posts about selenium.

install docco, then generate the html:

    npm install docco
    .node_modules/.bin/docco *.py

install markdown, then generate the html:

    brew install markdown #or whatever if you're not using homebrew on mac
    markdown blog-post-1.mkd > docs/blog-post-1.html
    markdown blog-post-2.mkd > docs/blog-post-2.html

now all the generated files live under docs/. Have fun.
