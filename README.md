# tic-tac-toe
Tic Tac Toe Web Application using Django

-- SET UP --

1. Clone the Repository
commands:
	git clone https://github.com/BhargaviLenka/TicTacToe.git
	cd tictactoe

2.Install Dependencies
Create a virtual environment and install the required packages:
commands:
	python -m venv venv
	source venv/bin/activate  # On Windows use `venv\Scripts\activate`
	pip install -r requirements.txt

3.Apply Migrations
Set up the database by applying the migrations:
commands:
	python manage.py migrate
	
4.Run the Development Server
Start the Django development server:
commands:
	python manage.py runserver

5.Access the Application
	Open a web browser and go to http://127.0.0.1:8000/ to use the application.

-- PROJECT STRUCTURE --

    index.html: The homepage where players enter their name to start the game.
    board.html: The game board where players make their moves.
    leaderboard.html: Displays the leaderboard with player statistics.
    static/: Contains static files like CSS and images.
    templates/: Contains HTML templates.
    views.py: Contains the view functions for handling game logic and rendering templates.
    urls.py: Defines URL patterns and routing.
    models.py: Contains the database models for Player and Game statistics.

-- PROJECT OVERVIEW --

This project is a simple web-based Tic-Tac-Toe game built using Django. Players can start a game, choose the difficulty level, and play against an AI opponent. The application also includes a leaderboard to track player statistics.
Features

    Play Tic-Tac-Toe against an AI with different difficulty levels.
    View and update a leaderboard with player statistics (wins, losses, and draws).
    Persistent player sessions with the ability to restart the game.
