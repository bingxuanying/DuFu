import sys


class Subscription:
    topics = set()

    def __init__(self):
        while True:
            try:
                zipcode = input("Enter zipcode to subscribe (enter DONE when finish): ")
                # Leave if DONE
                if zipcode == "DONE" or zipcode == "done":
                    break

                # Make sure user enters valid zipcode
                if zipcode in self.topics:
                    print("Failed => Topic already exists")
                elif len(zipcode) != 5 or not zipcode.isnumeric():
                    print("Failed => Invalid zipcode")
                else:
                    self.topics.add(zipcode)
                    print("Sucess => Subscribe Success!")
            
            except KeyboardInterrupt:
                sys.exit("Stop creating subscriber")