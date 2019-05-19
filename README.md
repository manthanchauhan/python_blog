# python_blog
A blogging website, meant to be used to share blog related to the Python programming language.
1. A superuser can upload blog and can attach certain related tags to each blog.
2. Any any visitor can view the list of blog, their author and times of creation.
3. Any authorized user can read a blog, comment on the blog or reply on any comment.
4. Each blog has an integrated discussion board automatically linked to it, for any comments.   

The project has 3 apps:
1. articles
2. boards
3. accounts

**articles app:**
This app has the following models,
1. Article
2. Tag

This app handles the following functionalities:
1. Creates Article from the blog content and thumbnail.
2. Lets a superuser to create Tags and link these tags to their blog.
3. Contains all the views related to Article and Tag model.

**boards app:**
This app has the following models,
1. Board
2. Post

and handles the following functionalities:
1. Creates a discussion board for each Article.
2. Lets any user to write comment in the discussion board.
3. Lets any user to reply to an existing comment.

**accounts app:**
This app handles all the authentication and user creation related tasks.

**Future plans:**
To add profiles support for each user.
