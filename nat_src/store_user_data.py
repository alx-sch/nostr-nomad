from class_nostr_format import Usr


def get_data_from_user(user: Usr):
	"""Parses the user_entries directory for user credentials."""
	
	priv_key_found = False
	pub_key_found = False
	relays_found = False

	# Parses the "ADD_PRIVATE_KEY_HERE.txt" file and stores the private key.
	with open(user.priv_key_path, "r", encoding="utf-8") as file:
		content = file.readlines()  # Read the whole file
		for line in content:
			if line.startswith('#') or line.startswith('\0') or line.startswith('\n'):
				continue
			user.priv_key = line.strip()
			priv_key_found = True
			break
		if (priv_key_found == False):
			return 1

	# Parses the "ADD_PUBLIC_KEY_HERE.txt" file and stores the public key.
	with open(user.pub_key_path, "r", encoding="utf-8") as file:
		content = file.readlines()  # Read the whole file
		for line in content:
			if line.startswith('#') or line.startswith('\0') or line.startswith('\n'):
				continue
			user.pub_key = line.strip()
			pub_key_found = True
			break
		if (pub_key_found == False):
			return 2

	# Parses the "ADD_RELAYS_HERE.txt" file and stores all the relays listed.
	with open(user.relays_path, "r", encoding="utf-8") as file:
		content = file.readlines()  # Read the whole file
		for line in content:
			if line.startswith('#') or line.startswith('\0') or line.startswith('\n'):
				continue
			user.relays.append(line.strip())
			relays_found = True
		if (relays_found == False):
			return 3

	return 0
