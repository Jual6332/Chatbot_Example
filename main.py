
from chatterbot import ChatBot

def main():
	print("Main function")

	chatbot = ChatBot("Animals University")

	exit_conditions = ("q","quit","exit")
	while True:
		query = input("> ")
		if query in exit_conditions:
			break
		else:
			print("{0}".format(chatbot.get_response(query)))

if __name__ == "__main__":
	main()