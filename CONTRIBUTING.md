# To start...
Hello there team!

Here's a few tips on how to work with this repo:

1. To clone the repo (which you only need to do once!)

git clone git@github.com:Hanami199/MLOpsProject.git
cd MLOpsProject

You could also use GitHub Desktop if you prefer!

2. Check out the branch
Each one of us will have a personal working branch (to keep things neat), on which we have to work on.
First we need to fetch all the branches:

git fetch origin

Then enter it using:

git checkout <branch-name>

3. Keep your work up to day
When you want to work on your part, also remember to keep your branch up to date using:

git fetch origin

git rebase origin/main

If there are conflicts, add the fixed files using git add <fixed-file> and then git rebase --continue, until all conflicts are resolved.

4. Saving your work
When you want to commit something new on the repo, do:

git add .
git commit -m "message"

Instead of message, write some words on what you did on those files (commit often if you feel like ti)

5. Push a Pull Request
When you want to push the things you modified and committed, do:

git push -u origin directory

On GitHub, you will also need to create a New pull request!

After the pull request is approved and a merge has occurred, remember to keep up to date! 
