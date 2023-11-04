echo "Get environments"
source ../env/bin/activate
echo "Start MyFinance application"
uvicorn main:app --reload