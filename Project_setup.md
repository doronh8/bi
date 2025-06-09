# Administration file
Contains all the Action Items which will assist you to manage Analytics Project

```dtd
mkdir  ppltx-tutorial
cd ppltx-tutorial
mkdir admin
```

## Create BigQuery Project
[How to set up BigQuery](https://www.youtube.com/watch?v=mWEP1BC_-FE&list=PLkKJj26K4JZ0CYuJY1jPCNJjLM2y0xZB2)<br>
[link to console ](https://console.cloud.google.com/bigquery?project=ll-data-training)

Create two projects in BigQuery
- ppltx-tutorial-dev
- ppltx-tutorial-prod

## Create Git Project
- [Watch Git Playlist - if needed](https://www.youtube.com/playlist?list=PLkKJj26K4JZ1zshdTXnb6cp7ge9BQlwKK)
- [Go to Git - if you already have an account](https://github.com/dashboard)
- use the directory name for the project

```dtd
echo "# ppltx-tutorial" >> README.md
git init
git add README.md
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/doronh8/ppltx-tutorial.git
git push -u origin main
```
- [Get personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

## Manage your Project repository
Create folders for
```dtd
mkdir tech jobs docs draft utilities
```

touch ./docs/readme.md

### [Add Git ignore file](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files)
```dtd
touch .gitignore
```
```dtd
# ignore all .a files
#*.a

# but do track lib.a, even though you're ignoring .a files above
#!lib.a

# only ignore the TODO file in the current directory, not subdir/TODO
#/TODO

# ignore all files in any directory named build
#build/

# ignore doc/notes.txt, but not doc/server/arch.txt
#doc/*.txt

# ignore all .pdf files in the doc/ directory and any of its subdirectories
#doc/**/*.pdf
```
```dtd
*pyc

draft/
```