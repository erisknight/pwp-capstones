class User(object):
    # takes user info
    def __init__(self, name, email):
        self.name = name  #string
        self.email = email  #string
        # empty dict that maps ratings to books
        self.books = {}

    # gets email for a user
    def get_email(self):
        return self.email

    # change email for a user
    def change_email(self, address):
        self.email = address
        return "Updated the email for {name} to: {address}".format(name=self.name, address=address)

    # allows pretty print of user info
    def __repr__(self):
        return "User {name} at {email}, books read: {books}".format(name=self.name, email=self.email, books=len(self.books))
    
    def books_read(self):
      return len(self.books)

    # compares two users
    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email
      
    # stores a book and optional rating for the user
    def read_book(self, book, rating=None):
      self.books[book] = rating

    # gives an average rating that this user has scored all books read
    def get_average_rating(self):
      book_count = 0
      book_score = 0
      for rating in self.books.keys():
        book_count += 1
        if self.books[rating] != None:
          book_score += self.books[rating]
      ave_rating = book_score/book_count
      return ave_rating

class Book(object):
  def __init__(self, title, isbn):
    self.title = title  #string
    self.isbn = isbn  #number
    self.ratings = []

  # fetches the book title
  def get_title(self):
    return self.title

  # fetches the book isbn
  def get_isbn(self):
    return self.isbn

  # fetches the title and author of a book
  def __repr__(self):
    return "{title}".format(title=self.title)

  # updates the ISBN for a given book title
  def set_isbn(self, new_isbn):
    self.isbn = new_isbn
    return "Updated the ISBN to {isbn}".format(isbn=new_isbn)

  # adds a rating to the book title
  def add_rating(self, rating):
    if rating > 0 and rating <= 4:
      self.ratings.append(rating)
    else:
      print("Invalid Rating")

  # compares two books
  def __eq__(self, other_book):
    #not sure, same question as eq users above
    return self.title == other_book.title and self.isbn == other_book.isbn

  # fetches the average rating for a book title
  def get_average_rating(self):
    all_ratings = 0
    for rating in self.ratings:
      all_ratings += rating
    if len(self.ratings) == 0:
      return "This book has not been rated"
    else:
      ave_rating = all_ratings/len(self.ratings)
    return ave_rating

  # creates a hash for the book dictionary to avoid unhashable list error
  def __hash__(self):
    return hash((self.title, self.isbn))

class Fiction(Book):
  def __init__(self, title, author, isbn):
    super().__init__(title, isbn)
    self.author = author

  # fetches the author name
  def get_author(self):
    return self.author

  # fetches the title and author of a book
  def __repr__(self):
    return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
  def __init__(self, title, subject, level, isbn):
    super().__init__(title, isbn)
    self.subject = subject  #string
    self.level = level  #string

  def get_subject(self):
    return self.subject

  def get_level(self):
    return self.level

  def __repr__(self):
    return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)
    # should probably return "the {level} manual.." for grammatical sake

class TomeRater(object):
  def __init__(self):
    self.users = {}
    self.books = {}

  # creates a Book
  def create_book(self, title, isbn):
    return Book(title, isbn)

  # creates a Fiction book
  def create_novel(self, title, author, isbn):
    return Fiction(title, author, isbn)

  # creates a NonFiction book
  def create_non_fiction(self, title, subject, level, isbn):
    return Non_Fiction(title, subject, level, isbn)

  # adds a read book to a user
  def add_book_to_user(self, book, email, rating=None):
    if email in self.users.keys():
      self.users[email].read_book(book, rating) # adds book to a user
      # if the book is in self.books, add 1 iteration of reading, else create book in self.books
      self.books[book] = self.books.get(book, 0) + 1
      if rating:
        book.add_rating(rating)
    else:
      return "No user with email {email}!".format(email=self.email)

  def add_user(self, name, email, user_books=None):
    # add a user to the dictionary
    if email in self.users:
      return "This reader already exists"
    else:
      self.users[email] = User(name, email) # adds new user
      if user_books != None:
        for book in user_books:
          self.add_book_to_user(book, email) # adds any books this user brings with them

  # prints the catalog of books read
  def print_catalog(self):
    for book in self.books.keys():
      print(book)

  # prints a list of users in our dictionary
  def print_users(self):
    for user in self.users.values():
      print(user)

  # finds the book read most
  def most_read_book(self):
    most_read = []
    total_reads = 0
    for book in self.books:
      times_read = self.books[book]
      if times_read > total_reads:
        total_reads = times_read
        most_read = book
    return most_read

  # gets the highest rated book
  def highest_rated_book(self):
    highest_rated = []
    rating = 0
    for book in self.books:
      if book.get_average_rating() > rating:
        rating = book.get_average_rating()
        highest_rated = book
    return "The highest rated book is {book} with a rating of {rating}.".format(book=highest_rated, rating=rating)  


  # gets the user with the highest average book rating
  def most_positive_user(self):
    most_positive = []
    high_rating = 0
    for user in self.users.values():
      ave_rating = user.get_average_rating()
      if ave_rating > high_rating:
        high_rating = ave_rating
        most_positive = user
    return "The most positive user is {name} with an average rating of {rating}.".format(name=most_positive, rating=high_rating)

  def get_n_most_read_books(self, n=3):
    # Returns the n books which have been read the most in descending order.
    if type(n) == int:
      decending_books = [book for book in sorted(self.books, key=self.books.get, reverse=True)]
      return "The {n} books read the most to the least often are: {books}".format(n=n,books=decending_books[:n])
    else:
      print("You must provide a whole number")
