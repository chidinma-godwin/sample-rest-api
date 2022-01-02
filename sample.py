# name=input("Enter your name:")
# print(name)
# year_of_birth=input("Enter your year of birth:")
# age=2021-int(year_of_birth)
# print(age)
users=[(0, "user1", "password1"), (1, "user2", "password2"), (2, "user3", "password3")]
user_mapping= {user[1]: user for user in users}
print(user_mapping)

# my_set= {1,2,4,3,3,5,5,7}
# print(my_set)
# for i in my_set:
#   print(i)

# print(sum([1,2,3,4,5]))

class Book:
  TYPES=("hardCover", "paperBack")

  def __init__(self, name, type, weight):
      self.name=name
      self.type=type
      self.weight=weight

  def __repr__(self):
      return f"<Book {self.name}, {self.type}, weighing {self.weight}g>"

  @classmethod
  def hardCover(cls, name, weight):
    return cls(name, cls.TYPES[0], weight+100)

  @classmethod
  def paperBack(cls, name, weight):
    return cls(name, cls.TYPES[1], weight)


book1=Book("Harry Porter", "some type", 1500)
book2=Book.hardCover("Harry Porter", 1500)
print(book1)
print(book2)

class BookShelf:
  def __init__(self, *books):
      self.books = books

  def __str__(self):
      return f"BookShelf with {len(self.books)} books"

shelf = BookShelf(book1, book2)
print(shelf)

user = {"name": "user1", "access_level": "admin"}

from functools import wraps

def secure_func(accesslevel):
  def decorator(func):
    @wraps(func)
    def secure():
      if user["access_level"] == accesslevel:
        return func()
    return secure
  return decorator

@secure_func("admin")
def get_admin_password():
  return "secret password"

@secure_func("guest")
def get_user_password():
  return "user password"

# password=secure_func(getPassword)
print(get_admin_password())
print(get_user_password())

