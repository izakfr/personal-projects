import poloniex_api_wrapper
import poloniex_auto_trader
import strings

class interface:
    def __init__(self, APIKey, Secret):
        self.strs = strings.strings()
        self.api = poloniex_api_wrapper.poloniex(APIKey, Secret)
        self.trader = poloniex_auto_trader.trader(self.api)

    def get_command(self):
        return raw_input("Enter a command: ")

    # Welcome menu commands
    def welcome_menu_print(self, menu):
        if(menu == "main"):
            print(self.strs.main_menu)
        elif(menu == "recommendations"):
            print(self.strs.recommendations_menu)


    # Main menu commands
    def main_command(self, command):
        if(command == "help"):
            print(self.strs.main_help_command)
            return "main"
        if(command == "recommendations"):
            return "recommendations"


    # Recommendations menu commands
    def should_sell_command(self):
        currencyPair = raw_input("Enter a currency pair: ")
        margin = int(raw_input("Enter a gain margin (%): ")) * .01
        print(self.trader.should_sell(self.api, currencyPair, margin, .2))
        return 0

    def return_balances(self):
        currency = raw_input("Enter a currency: ")
        print(self.trader.return_balances(self.api, currency))
        return 0

    # A command was called while in the recommendations menu, we deal with the
    # command with this function below
    def recommendations_command(self, command):
        if(command == "help"):
            print(self.strs.recommendations_help_command)
            return "recommendations"
        elif(command == "should_sell"):
            self.should_sell_command()
            return "recommendations"
        elif(command == "return_balances"):
            self.return_balances()
            return "recommendations"




def program():
    private_data = open("keys.txt", "r")
    APIKey = private_data.readline().rstrip('\n')
    secret = private_data.readline().rstrip('\n')

    inter = interface(APIKey, secret)
    menu = "main"
    prev_menu = "main"

    inter.welcome_menu_print(menu)

    while(1):
        if(prev_menu != menu):
            inter.welcome_menu_print(menu)

        command = inter.get_command()
        if(command == "exit"):
            break

        if(menu == "main"):
            prev_menu = menu
            menu = inter.main_command(command)

        elif(menu == "recommendations"):
            prev_menu = menu
            menu = inter.recommendations_command(command)


    return 0

if __name__ == "__main__":
    program()
