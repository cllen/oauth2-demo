class ExamplePermissions:
	USER = 0x01 * 2 ** 0
	ADMINISTER = 0x01 * 2 ** 1

if __name__ == '__main__':
	print(ExamplePermissions.USER | ExamplePermissions.ADMINISTER)
	print(3 & ExamplePermissions.USER == ExamplePermissions.USER)