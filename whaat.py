from whaaaaat import prompt, print_json

questions = [
    {
        'type': 'list',
        'name': 'first_name',
        'message': 'What\'s your first name',
        'choices': ["Jake", "Megan", "Pussy"],
    }
]

answers = prompt(questions)
print_json(answers)  # use the answers as input for your app
