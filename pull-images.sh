for image in `cat .env | grep _VERSION | awk -F= '{ print $2 }' `
do 
  docker pull $image
done