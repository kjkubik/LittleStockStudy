class Document:
    """
    This class represents a document with a title and content.
    
    Attributes:
        title (str): The title of the document.
        content (str): The content of the document.
    
    Methods:
        __init__(title, content): Initializes the document with a title and content.
        get_summary(): Returns a brief summary of the document.
        display(): Displays the full document.
    """
    
    def __init__(self, title, content):
        """
        Initializes the document with a title and content.
        
        Parameters:
            title (str): The title of the document.
            content (str): The content of the document.
        """
        self.title = title
        self.content = content
    
    def get_summary(self):
        """
        Returns a brief summary of the document (first 100 characters).
        
        Returns:
            str: A summary of the document.
        """
        return self.content[:100] + "..." if len(self.content) > 100 else self.content
    
    def display(self):
        """
        Displays the full document, including the title and content.
        """
        print(f"Title: {self.title}")
        print(f"Content: {self.content}")

# Example of using the Document class
doc = Document("Title of Document", "Whatever you want to tell about the doc here; but first put summary then " 
               "the details because the summary will only get the first 100 chars you write. I will show you "
               "what I mean because I am attempting to go much further than this."
               )
               
print(doc.get_summary())  # Output will be the first 100 characters of the content
doc.display()  # Output will show the full title and content
