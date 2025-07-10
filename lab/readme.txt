
Run frontend:

		build image:
		   docker build -t server_app .

		Run image as container :
		docker run -p 9012:9012 server_app

		Visit :
		http://localhost:9012


		docker exec -it <container ID> <Command>
