##to run:

git clone the_git_url_here

pip install -r requirements.txt


It's setup to use postgre, so use this tutorial as well if you're on ubuntu 14.04

read installation and basic setup here:
https://help.ubuntu.com/community/PostgreSQL

python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver

If you're interested in creating a nice and simple blog like this one with flask, go check out Miguel Grinberg's excellent book, "Flask Web Development"



also, if you're looking to create a blog, then I highly recommend using jekyll and github pages. There's really nothing a simple blog cant be done with a static site. (Wufoo for contact and mailchimp for subscriptions)
