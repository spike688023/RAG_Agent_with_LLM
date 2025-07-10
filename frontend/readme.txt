install docker:
brew install colima
brew install docker
colima start

upgrad gradio:

pip install --upgrade gradio_client


Run frontend:

		build image:
		   docker build -t my-python-webapp .

		Run image as container :
		docker run -p 8090:8090 my-python-webapp

		Visit :
		http://localhost:8090


		docker exec -it <container ID> <Command>
