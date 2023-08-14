class Category:
    def __init__(self, description):
        """
        Initializes a Category instance with a given description.
        """
        self.description = description
        self.ledger = []  # A list to store financial transactions
        self.__balance = 0.0  # Private attribute to track the balance

    def __repr__(self):
        """
        Returns a formatted representation of the Category instance, including the ledger and total balance.
        """
        header = self.description.center(30, "*") + "\n"
        ledger = ""
        for item in self.ledger:
            # Format and truncate description and amount for ledger entry
            line_description = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        total = "Total: {:.2f}".format(self.__balance)
        return header + ledger + total

    def deposit(self, amount, description=""):
        """
        Adds a deposit transaction to the ledger and updates the balance.
        """
        self.ledger.append({"amount": amount, "description": description})
        self.__balance += amount

    def withdraw(self, amount, description=""):
        """
        Adds a withdrawal transaction to the ledger and updates the balance if funds are sufficient.
        Returns True if successful, False otherwise.
        """
        if self.__balance - amount >= 0:
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.__balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        """
        Returns the current balance of the category.
        """
        return self.__balance

    def transfer(self, amount, category_instance):
        """
        Transfers funds from this category to another category.
        Returns True if successful, False otherwise.
        """
        if self.withdraw(amount, "Transfer to {}".format(category_instance.description)):
            category_instance.deposit(amount, "Transfer from {}".format(self.description))
            return True
        else:
            return False

    def check_funds(self, amount):
        """
        Checks if the category has sufficient funds for a given amount.
        Returns True if sufficient funds are available, False otherwise.
        """
        if self.__balance >= amount:
            return True
        else:
            return False


def create_spend_chart(categories):
    """
    Creates a spend chart displaying the percentage spent in each category.
    """
    spent_amounts = []
    # Calculate total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.description, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")
