import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re  # Import the re module for regular expressions
import tkinter as tk

def save_values():
    global base_trade_amount, desired_profit
    base_trade_amount = int(entry_base_trade.get())
    desired_profit = float(entry_desired_profit.get())
    root.destroy()

def create_input_window():
    global root, entry_base_trade, entry_desired_profit

    # Create the main window
    root = tk.Tk()
    root.title("Trade Inputs")

    # Create labels and entry widgets
    label_base_trade = tk.Label(root, text="Starting Investing Amount:")
    label_base_trade.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_base_trade = tk.Entry(root)
    entry_base_trade.grid(row=0, column=1, padx=10, pady=10)

    label_desired_profit = tk.Label(root, text="Exit Balance:")
    label_desired_profit.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    entry_desired_profit = tk.Entry(root)
    entry_desired_profit.grid(row=1, column=1, padx=10, pady=10)

    # Create a button to save values
    save_button = tk.Button(root, text="Save", command=save_values)
    save_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Run the Tkinter main loop
    root.mainloop()



def enter_value(driver: webdriver, amount: str):
    """Find input field and enter trading amount"""
    trade_field = driver.find_element(By.XPATH, '//input[@class="input-control__input"]')
    trade_field.send_keys(Keys.CONTROL + 'A', Keys.BACKSPACE)
    for char in amount:
        trade_field.send_keys(char)
        sleep(random.choice([0.1, 0.2, 0.3, 0.4, 0.5]))
    trade_field.send_keys(Keys.ENTER)

def click_button(button, driver: webdriver):
    """Wait for a new trade to start and click the provided button"""
    print("Waiting for new trade to start")
    while True:
        timer = float(driver.find_element(By.XPATH, '//div[@class="server-time online"]').text.split()[0][-2:])
        if 0 <= timer <= 1:
            button.click()
            break
        sleep(0.1)

def get_profit_loss(driver):
    """Get profit or loss from the trade outcome"""
    try:
        profit_loss = driver.find_element(By.XPATH, "//div[@class='trades-notifications-item']").text
        result = re.search(r'(\d+\.\d+)', profit_loss)
        return result.group(0) if result else None
    except Exception as e:
        print(f"Error while getting profit/loss: {e}")
        return None

def click_random_button(driver, buttons):
    """Click a random button from the provided list"""
    random_button = random.choice(buttons)
    random_button.click()

def wait_for_new_trade(driver):
    """Wait for a new trade to start"""
    print("Waiting for new trade to start")
    while True:
        timer = float(driver.find_element(By.XPATH, '//div[@class="server-time online"]').text.split()[0][-2:])
        if 0 <= timer <= 1:
            break
        sleep(0.1)

def calculate_profit(driver, current_profit):
    """Calculate and update the current profit based on the demo account money"""
    # Find the demo account money element
    demo_account_money = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div/div[3]/div[2]")

    # Get the text and convert it to a float
    dollars = demo_account_money.text
    previous_demo_account_money = float(dollars[1:].replace(',', ''))

    # Calculate the profit
    profit = previous_demo_account_money - current_profit

    # Update the current profit
    current_profit += profit

    # Print the results
    print(f"Profit after trade: ${profit}")
    print(f"Current Profit: ${current_profit}")

    # Return the updated current profit
    return current_profit

def check_desired_profit(current_profit, desired_profit):
    """Check if the desired profit is reached and quit the program if true"""
    if current_profit >= desired_profit:
        print(f"Desired profit of ${desired_profit} reached. Stopping the program.")
        driver.quit()
        exit()



def main_trading_logic(driver, base_trade_amount, desired_profit, martingale_multiplier):
    reset_trade_amount = base_trade_amount

    # # Main program
    # # Call the function to create the input window
    # create_input_window()

    # # Now, you can use the values of base_trade_amount and desired_profit in your program.
    # print("Base Trade Amount: $", base_trade_amount)
    # print("Desired Profit: $", desired_profit)
    # base_trade_amount = int(input("Please enter the base trade amount: $"))
    # desired_profit = float(input("Enter the profit you want: $"))
    # reset_trade_amount = base_trade_amount
    martingale_multiplier = 2
    URL = "https://qxbroker.com/en/demo-trade"
    ID = 33614570
    # driver = uc.Chrome()
    # driver.get(URL)
    # driver.maximize_window()
    current_profit = 0

    USERNAME = "htssuppliers@gmail.com"
    PASSWORD = ""

    # with open("pass.txt", "r") as file:
    #     PASSWORD = file.readline()
    # Implicitly wait for 30 seconds for elements to appear
    driver.implicitly_wait(30)
    # input()
    # Find and enter the username
    username = driver.find_element(By.XPATH, "/html[1]/body[1]/bdi[1]/div[1]/div[1]/div[2]/div[3]/form[1]/div[1]/input[1]")
    username.send_keys(USERNAME)

    # Enter the password
    password = driver.find_element(By.XPATH, "/html[1]/body[1]/bdi[1]/div[1]/div[1]/div[2]/div[3]/form[1]/div[2]/input[1]")
    # password.send_keys(PASSWORD)  # Use the actual password here
    password.send_keys("Junaid")
    password.send_keys(Keys.ENTER)

    sleep(5)

    # Click on the user menu
    user_menu = driver.find_element(By.XPATH, "//div[@class='usermenu__info-wrapper']")
    user_menu.click()
    sleep(3)

    # Get the user ID and check if it matches the expected ID
    web_id = driver.find_element(By.XPATH, "//span[@class='usermenu__number']")
    web_id = int(web_id.text.split()[-1])

    if web_id != ID:
        print("User ID does not Exist, BYE!")
        driver.quit()
        exit()
    else:
        print("User ID Found")
        driver.get(URL)

    sleep(2)

    # Define the buttons for trading
    buttons = [
        driver.find_element(By.XPATH, "/html/body/div/div/div[1]/main/div[2]/div[1]/div/div[6]/div[4]"),  # Down button
        driver.find_element(By.XPATH, "//div[@class='section-deal__success  percent']")  # Up button
    ]

    # Assuming driver is already initialized and current_profit is defined
    current_profit = calculate_profit(driver, current_profit)

    # Enter the initial trade amount
    enter_value(driver, str(base_trade_amount))

    # Main trading loop
    while True:
        # Assuming desired_profit is already defined
        if check_desired_profit(current_profit, desired_profit):
            break

        # Wait for a new trade to start
        wait_for_new_trade(driver)

        print("Executing trade")
        # Click a random trading button
        click_random_button(driver, buttons)

        # Check the outcome of the trade
        while True:
            sleep(0.1)
            try:
                loss = get_profit_loss(driver)

                if loss == '0.00':
                    print("Trade Lost!")
                    print("Using Martingale Strategy")
                    sleep(0.1)
                    base_trade_amount *= martingale_multiplier
                    enter_value(driver, str(base_trade_amount))
                    sleep(0.1)
                    break
                else:
                    print("Trade Won!")
                    enter_value(driver, str(reset_trade_amount))
                    base_trade_amount = reset_trade_amount 
                    sleep(0.1)
                    break

            except:
                pass

    driver.quit()


def main():
    # Call the function to create the input window
    create_input_window()

    # Now, you can use the values of base_trade_amount and desired_profit in your program.
    print("Base Trade Amount: $", base_trade_amount)
    print("Desired Profit: $", desired_profit)

    # # Get additional user input or set other parameters as needed
    martingale_multiplier = 2

    # Call the function to check the license and execute the main trading logic
    license_start = "23-12-23"
    days_of_license = 120
    today = datetime.today()
    license_start_date = datetime.strptime(license_start, "%y-%m-%d")

    delta = today - license_start_date
    if delta.days < days_of_license:
        print(f"License expires in {days_of_license - delta.days} days")
        with uc.Chrome() as driver:
            driver.get("https://qxbroker.com/en/demo-trade")
            driver.maximize_window()
            # current_profit = 0
            main_trading_logic(driver, base_trade_amount, desired_profit, martingale_multiplier)
    else:
        print("License Expired")

if __name__ == "__main__":
    main()
