import hashlib
import random
import re

solutions = [
	{
		"hash": "06df05371981a237d0ed11472fae7c94c9ac0eff1d05413516710d17b10a4fb6f4517bda4a695f02d0a73dd4db543b4653df28f5d09dab86f92ffb9b86d01e25",
		"regular_expression": r"^\d+$",
		"re_error_message": "Only Numbers Accepted!"	
	},
	{
		"hash": "9307b40966fc5ba841aca6ed8010812b23a75db31430ed707ba7870f43a5bd6069a8a1c338aac3527582cc48af1051a108844a3bb56e648c016439a7389afcca",
		"re_error_message": "Enter IP Address!",
		"regular_expression": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
	},
	{
		"format_": "IP-(packet count), ex: 10.11.252.85-2932",
		"hash": "778f0cea5472f9f4fd9641739fafc31c95db474c4879a4c222fc807ab877f535f1a0dec655589a62208d6e033df61bfa2cef26e702f5ac3f1c328ca5c6e40b2b",
		"regular_expression": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d+$",
		"re_error_message": "Invalid format!!",
	},
	{
		"hash": "271bc86ae36225e06b7322b9ef59efbfa2430892acfcba861d84ae39c896d3218013589642bd8d36b9cc3a4b6addf196f29cef770bf2a7694a1b8ca507a7fe2b",
		"regular_expression": "[a-zA-Z0-9]+",
		"re_error_message": "Only letters and nubmers allowed!",
		"rule": "lambda x: x.lower()"
	},
	{
		"hash": "22311c9a91d5232795404f3c70bff930583f572da3339ee2ff3df5a5bac86e8f9a72c837501bf8c4b2721aa14fac7fc97955542c0f3d7eed7b2c5a3323086adb",
		"re_error_message": "Enter IP Address!",
		"regular_expression": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
	},
	{
		"hash": "7c4a6f22a138b86cdfc65c6b48524e557fa43843be9fc8c4d6e06133ec11888e580e1a1b5843c6065bf973791e2f71a41ff90a5230c0e4c6b6c62d74ff413f02",
		"re_error_message": "Enter IP Address!",
		"regular_expression": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
	},
	{
		"hash": "8233491803375c41e3cdecd53d8c24029f647ea19cb10844b8fe7034e969138ef5ea168bcc2f1ee73e4136b4cdaa0518bd917c1e183c03aaccd6c629c4e1b639",
		"re_error_message": "Invalid date format!",	
		"format_": "UTC format: YYYY-mm-DD HH-MM-SS, ex: 1993-08-26 21:52:07",
		"regular_expression": r"^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d$"
	},
	{
		"hash": "14fb54d8e8407fb4396dedae4f1d69f7465d7ed628ebfd39c4d3dbc163a34c914ff97f7c52dfff1ed14efbc9bcfb28c0625ac26d17a901f95331736c07ee0a79",
		"re_error_message": "Enter IP Address!",
		"regular_expression": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
	},
	{
		"hash": "1365d8f5c5aef10d1c410ce1fe5b05926ee3eab383abefd55a5415a365b5289fe012dc354641db867f861f28a26b75a77b481418e5c4bda768b078dcbb9737d6",
	},
	{
		"hash": [
			"cca1e6dd6d0ca30aeea095b0e6595de3bb025f5f2776e1fb05382d804db43b851f4d92106756d57bf8c25cf2fa28274fa2d9a9e0fd656687d5cff76ef21b5de2",
			"d3031349b4a56d2ea71410854b563776497c2c763272898ada818ca548b221a1c84c43bb973ecacc188118adf7f8153dfce758713811b8ad4e17f31c38f11d65",
		],
	},
	{
		"hash": "f28dbe4e598a7c2f5a049083ce593b02e38378c827cca7250d08ee1f3e5c9e9670c200ce6b086aff0ce1466dfaaa7cc0ed56ee274de64da9c81a43ba7d1c950e",
		"re_error_message": "Enter IP Address!",
		"regular_expression": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
	},
]


class Solution():
	def __init__(self, hash, regular_expression=None, re_error_message=None, rule=None, format_=None):
		self.hash = hash
		self.preprocess = eval(rule) if rule is not None else None
		self.error = re_error_message
		self.format = format_
		self.matcher = re.compile(regular_expression) if regular_expression is not None else None

	def valid(self, input_):
		return self.matcher is None or self.matcher.match(input_) is not None

	def check(self, input_):
		if self.preprocess is not None:
			input_ = self.preprocess(input_)
		input_hash = hashlib.sha512(input_.encode()).hexdigest()
		if isinstance(self.hash, list):
			return input_hash in self.hash
		return input_hash == self.hash

def get_input(msg):
	result = ""
	while not result:
		result = input(msg)
	return result.strip()


def main():
	print("[*] Enter 'exit' for close the program!")
	print(f"[*] Index of available questions: {', '.join([str(i) for i in range(1,len(solutions)+1)])}")
	while (result := get_input("Enter index: ")) != "exit":
		try:
			index = int(result)-1
			solution = Solution(**solutions[index])
		except (IndexError, ValueError):
			print("[-] Invalid index")
			continue

		user_solution = get_input(
				f'[*] Enter the answer of question {index+1}{" [format: " + solution.format + "]" if solution.format is not None else ""}: '
			)

		if not solution.valid(user_solution):
			print(f"[-] {solution.error}")
			continue

		if solution.check(user_solution):
			print("[+] Currect answer :)))")
		else:
			print("[-] Answer is not currect ¯\\_(ツ)_/¯")


if __name__ == "__main__":
	main()
