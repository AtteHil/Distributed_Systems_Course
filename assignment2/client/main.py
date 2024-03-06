import xmlrpc.client
class NotebookClient:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy('http://localhost:8000')

    def add_note(self):
        topic = input("Enter the topic of the note: ")
        name = input("Enter the name of the note: ")
        text = input("Enter the text of the note: ")
        response = self.server.addNote(topic, name, text)
        if(response):
            print("Note added succesfully!")

    def get_notes_by_topic(self):
        topic = input("Enter the topic to retrieve notes: ")
        notes = self.server.getNotesByTopic(topic)
        if notes:
            print(f"\nNotes for topic '{topic}':")
            for note in notes:
                print(f"Name: {note['note']}")
                print(f"Timestamp: {note['timestamp']}")
                print(f"Text: {note['text']}\n")
        else:
            print(f"No notes found for topic '{topic}'")
    def findFromWikipedia(self):
        searchTerm= input("Enter the search word from wikipedia: ")
        topic= input("Enter the topic you want this information to be added: ")
        information = self.server.findFromWikiApi(searchTerm, topic)
        if information:
            print("Data found and added to topic.")
        
if __name__ == '__main__':
    client = NotebookClient()
    while True:
        print("\nMenu: ")
        print("1. Add a note")
        print("2. Get notes")
        print("3. Find from wikipedia and and add to topic")
        print("4. Exit")
        selection = input("What you want to do: ")
        match selection:
            case "1":
                client.add_note()
            case "2":
                client.get_notes_by_topic()
            case "3":
                client.findFromWikipedia()
            case "4":
                break
            case _:
                print("Invalid selection. Try again!")