# Main File

import checks
import bot
import ease

if __name__ == '__main__':
    print('Running the Syndra Project! If you need any assistance, please contact the developer or create an issue on the GitHub repository. Thank you! \n ')
    
    ease.print_line()

    with open('ASCII.txt', 'r') as file:
        print(file.read())

    ease.print_line()

    checks.env()
    checks.db()
    bot.main()

# Path: src/main.py