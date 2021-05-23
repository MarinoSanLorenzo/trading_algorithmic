echo "Start pushing your project to Github!"
git add .
read -p "Commit message: " msg
git commit -m $msg
branch=dev
read -p "Do you want to commit on branch $branch [y]?" answer
if [[ answer=y ]]; then
	git push origin $branch
	echo "Code pushed successfully to $branch"
else
	echo "Commit aborted"
fi

