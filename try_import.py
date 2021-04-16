from data_ops import msg_handler


def main():

	msg = {"type":"read", "method":"view_cart", "username":"vasu"}
	ret = msg_handler(msg)
	print(ret)

if __name__ == '__main__':
	main()