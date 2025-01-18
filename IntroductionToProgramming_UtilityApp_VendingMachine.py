import pygame
import pyttsx3
import time
import sys

# Initialize pygame mixer and pyttsx3 engine
pygame.mixer.init()
engine = pyttsx3.init()

# Setup talk-to-speech feature
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use female voice
engine.setProperty('rate', 130)  # Speech rate

def typing(text, delay=0.1): # Typing effect
    for char in text:
        sys.stdout.write(char)  # Write character without a newline
        sys.stdout.flush()  # Flush the output buffer to print the character immediately
        time.sleep(delay)  # Wait for the specified delay before printing the next character
    print()  # Print a newline at the end

def play_background_music(): # Plays background music
    try:
        music_file = "C:\\Users\\MICHELLE\\Music\\BGM\\Escape from reality in Kyoto on the weekend.mp3"  # Music file
        pygame.mixer.music.load(music_file)  # Load the music
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.0)  # Loop the background music
    except pygame.error as e:
        print(f"[Error loading music: {e}]")

def stop_background_music(): # Stops the background music
    pygame.mixer.music.stop()

def speak(text): # Text-to-speech function
    engine.say(text)
    engine.runAndWait()

def display_items(vm_items): # Display function for the vending machine items, price and stock info
    speak("Available items are:")
    print("\n[Available Items:]")
    for code, items in vm_items.items():
        print(f"{code}: {items['item']} - AED {items['price']} - (Stock: {items['stock']})")

def item_stock(vm_items, code): # Stock management
    return code in vm_items and vm_items[code]['stock'] > 0

def transaction(vm_items, code, payment): # Function for transaction and giving change
    sel_item = vm_items[code]
    price = sel_item['price']
    if payment < price:
        speak("Payment Insufficient! Please insert more money next time.")
        print("\n[Payment Insufficient! Please insert more money next time.]")
        return False, 0

    change = payment - price
    sel_item['stock'] -= 1  # Reduce stock
    return True, change

def handle_payment(): # Function for payment and input validation
    while True:
        try:
            speak("Please insert your payment.")
            payment = float(input("\n[Please insert your payment:] \nAED: "))
            if payment <= 0:
                speak("Invalid amount! Payment must be a positive value.")
                print("[Invalid Amount! Please try again.]")
                continue
            return payment
        except ValueError:
            speak("Invalid amount! Please enter a valid number.")
            print("[Invalid amount! Please try again.]")

def print_receipt(transactions): # Function to print receipt
    header = "\n[--------------- Receipt --------------]"
    total_price = 0
    receipt_details = ""  # Initialize an empty string to store the receipt details
    for transaction in transactions:
        ts = f"Item: {transaction['item']} | Price: AED {transaction['price']} | Change: AED {transaction['change']:.2f}"
        receipt_details += ts + "\n"  # Concatenate each transaction line to the receipt
        total_price += transaction['price']

    tp = f"\nTotal: AED {total_price:.2f}"
    footer = "\n[----------- End of Receipt -----------]"
    receipt = header + "\n" + receipt_details + tp + footer
    typing(receipt, delay=0.02)

def play_receipt_sound(): # Function to play receipt printing sound
    try:
        receipt_sound = "C:\\Users\\MICHELLE\\Downloads\\receipt.mp3"
        pygame.mixer.Sound(receipt_sound).play()  # Play the sound
    except pygame.error as e:
        print(f"[Error playing receipt sound: {e}]")

def main(): #Main function to run the whole program
    vm_items = {
        'A1': {'item': 'Chips', 'price': 3.20, 'stock': 17},
        'A2': {'item': 'Energy Bar', 'price': 5.00, 'stock': 24},
        'A3': {'item': 'Chocolate Bar', 'price': 3.15, 'stock': 18},
        'A4': {'item': 'Candy', 'price': 3.00, 'stock': 19},
        'A5': {'item': 'Fruit Snack', 'price': 3.95, 'stock': 21},
        'B1': {'item': 'Soda', 'price': 3.50, 'stock': 13},
        'B2': {'item': 'Water', 'price': 1.00, 'stock': 25},
        'B3': {'item': 'Juice', 'price': 3.95, 'stock': 22},
        'B4': {'item': 'Sports Drink', 'price': 5.00, 'stock': 19},
        'B5': {'item': 'Sparkling Water', 'price': 3.95, 'stock': 14}
    }

    transactions = []  # List to store transactions during the session

    play_background_music() # Play background music
    speak("Welcome to the Vending Machine!") # Welcome greetings
    text = "[----- Welcome to the Vending Machine! -----]" # Welcome header
    typing(text, delay=0.05)

    while True:
        display_items(vm_items) # Call display_items function with items

        speak("Please enter the code of the item you'd like to purchase or press 'Q' to exit.")
        pick = input("\nPlease enter the code of the item you'd like to purchase (e.g., A1, B1, etc.) or 'Q' to exit: ").upper() # Input for user item of choice

        if pick == "Q":
            speak("Thank you for using the vending machine. Goodbye!")
            print("[Thank you for using the vending machine. Goodbye!]")
            stop_background_music()  # Stop music when exiting
            play_receipt_sound()  # Play the receipt sound
            print_receipt(transactions)  # Print the receipt and exit the program
            break

        if not item_stock(vm_items, pick):
            speak("Item not found or out of stock. Please choose a valid item.")
            print("\n[Item not found or out of stock. Please choose a valid item.]")
            continue

        sel_item = vm_items[pick] 
        print(f"\n[Item Selected: --- {sel_item['item']} -- Price: AED{sel_item['price']}]")

        payment = handle_payment()

        success, change = transaction(vm_items, pick, payment)

        if success:
            speak(f"Thank you for your purchase! Your change is AED {change:.2f}.")
            print(f"\n[Thank you for your purchase!] \n[Your change is: AED{change:.2f}]")
            transactions.append({'item': sel_item['item'], 'price': sel_item['price'], 'change': change})  # Add transaction details to the list
        else:
            print("[Transaction Failed! Not Enough Funds.]")

if __name__ == "__main__":
    main()
