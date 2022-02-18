from applications import create_app 
from etc import Configuration

app = create_app(Configuration)

if __name__ == '__main__':
	app.run(debug=True)


