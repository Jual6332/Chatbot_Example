
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import JsonFileTrainer

def main():
	print("Main function")

	chatbot = ChatBot("Detroit Zoo")

	'''
	trainer = ListTrainer(chatbot)
	# The .train() function injects entries into your database to build upon 
	# the graph structure that Chatterbot uses to choose possible replies.
	trainer.train([
		"Hi",
		"Welcome, friend"
	])
	trainer.train([
		"Are you a plant?",
		"No, I am an owl! Your guide to Animals University - in computer form!"
	])'''

	trainer = JsonFileTrainer(
		chatbot,
		field_map={
			'text':'text',
			'in_response_to':'in_response_to',
			'persona':'persona',
			'conversation':'conversation'
		}
	)

	trainer.train('./data/training_data.json')

	exit_conditions = ("q","quit","exit")
	while True:
		query = input("> ")
		if query in exit_conditions:
			break
		else:
			print("{0}".format(chatbot.get_response(query)))

if __name__ == "__main__":
	main()