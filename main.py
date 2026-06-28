
from chatterbot import ChatBot
import json
import os
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import JsonFileTrainer

def build_training_pairs(json_path: str) -> list:
	"""	
	Converts the conversation JSON into flat [input, response] pairs
	that ListTrainer expects. Each bot entry with a valid in_response_to
	becomes its own pair, so multiple user phrasings can map to the
	same bot reply without creating conflicting DB entries.
	"""
	with open(json_path, "r") as f:
		data = json.load(f)

	pairs = []
	for entry in data.get("conversation", []):
		persona = entry.get("persona", "")
		text = entry.get("text", "").strip()
		in_response_to = (entry.get("in_response_to") or "").strip()

		if persona == "bot" and text and in_response_to:
			pairs.append([in_response_to, text])

	return pairs

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

	# Changed from JsonListTrainer to ListTrainer. 
	# JsonListTrainer was the root cause of the bad responses since it chains entries sequentially instead of as clean input→output pairs.
	trainer = ListTrainer(chatbot)

	pairs = build_training_pairs("./data/training_data.json")

	if not pairs:
		print("⚠️  No training pairs found — check your JSON file.")

	print("Training on {0} Q→A pair(s)...".format(len(pairs)))
	for user_msg, bot_reply in pairs:
		trainer.train([user_msg, bot_reply])
		print("  ✓  '{0}' → '{1}'".format(user_msg[:60],bot_reply[:60]))
	print("Training complete.\n")

	exit_conditions = ("q","quit","exit")
	while True:
		query = input("> ")
		if query in exit_conditions:
			break
		else:
			print("{0}".format(chatbot.get_response(query)))
			# Confidence score shown during dev so you can tune the threshold.
            # Swap for the simpler line below once accuracy is satisfactory:
            #   print(f"{response}")
			#print("[{0}] {1}".format(response.confidence:.2f,response))

if __name__ == "__main__":
	main()