# code written by Adnan Rehman

import sys
import os

class Person(object): #person object stores each individuals name and birthday
  fname = ""
  lname = ""
  month = ""
  day = ""
  year = ""
  def __init__(self, fname, lname, month, day, year): #constructor for person initializes instance variables
    self.fname = fname
    self.lname = lname
    self.day = day
    self.month = month
    self.year = year
        
class BirthdayBook(object): #birthdaybook object stores birthdaybooks
  book = []
  def __init__(self):
    self.book = [] #create a new list of books for every BirthdayBook object
    
  def add(self, person):
    "add the person to the list of Persons"
    self.book.append(person) #add new person object to the end of the list
    
  def list(self):
    if len(self.book) == 0:
      print("There are no entries in the birthday book")
    for i in range(len(self.book)):
      print("%s. %s %s %s/%s/%s" % (i+1, self.book[i].fname, self.book[i].lname, self.book[i].month, self.book[i].day, self.book[i].year))
      
  def delete(self, index):
    "delete a person from the birthday book"
    index = int(index)
    if index > len(self.book) or index <= 0:
      print('That entry does not exist, current entries in the birthday book are:')
      self.list()
    else:
      print('Really delete %s %s from the birthday book? (y/n)' % (self.book[int(index)-1].fname, self.book[int(index)-1].lname))
      decision = input().lower()
      while (decision != 'n' and decision != 'y'): #keep asking until the user enters yes or no 
        print('Really delete %s %s from the birthday book? (y/n)' % (self.book[int(index)-1].fname, self.book[int(index)-1].lname))
        decision = input().lower()
      if (decision == 'y'):
        del self.book[int(index)-1] #index-1 to account for 0 indexing
        print('Deleted')
      
  def search(self, name):
    "search the birthday book for a first or last name and return all entries matching, if any"
    matching_names = [] #create a new empty list at every function call, this will store any matches of parameter name with names in the birthday book
    for i in self.book:
      if name.lower() == i.fname.lower() or name.lower() == i.lname.lower(): #make sure it is not case sensitive by making everything lowercase
        matching_names.append(i) #if name matches, append it to the list of names
    if len(matching_names) == 0:
      print("I'm sorry, but there are no entries with a name of %s" % name)
    else:
      print("Entries with a name of %s" % name) #print all matching entries
      for i in range(len(matching_names)):
        print("%s. %s %s %s/%s/%s" % (i+1, matching_names[i].fname, matching_names[i].lname, matching_names[i].month, matching_names[i].day, matching_names[i].year))
        
  def save(self, filename):
    f = open("%s" % filename, "w") #open filename with 'write' enabled
    for i in range(len(self.book)):
      f.write("%s %s %s %s %s %s\n" % (i+1, self.book[i].fname, self.book[i].lname, self.book[i].month, self.book[i].day, self.book[i].year)) #add all the people to the file
    f.close() #good practice to close file after use
    print("Saved birthdays to %s " % filename)
   
  
  def load(self,filename): 
    tempBook = self.book         #hold the current birthdaybook in case load is unsuccessful
    try:                         #this try clause will catch any error python encounters while trying to open the file, we deal with it in the 'except:' clause
      f = open("%s" % filename)
      try:       #this try clause will catch any error python encounters while trying to convert the text from the file into person objects 
        count = 1           
        self.book = []           #we delete the list to avoid appending the new bdaybook to the previous one
        for line in f:
          line.strip('\n')       #separate the text in the line and remove the newline character so we dont have to worry about processing it
          line = line.split()
          if int(line[0]) != count:
            raise IndexError     #if the persons in the file are numbered incorrectly (i.e. it was not saved by this program) it will force python to have an error
          else:
            self.add(Person(line[1],line[2],line[3],line[4],line[5])) #otherwise add the person to the birthday book
          count += 1
        print("Birthdays in '%s' added to birthday book" % filename) 
      finally:                   #regardless of any errors, we always want to close the file after were done (finally clause)
        f.close()
    except (IndexError, ValueError): #except clause is where we deal with the errors. instead of python crashing, we can accept errors and continue running the program, we just let the user know there was a problem  
      print("Error: '%s' is not in the correct format. You can only load files saved by this same program" % filename) #these errors are from incorrectly formatted text files 
      print("Loading previous birthdaybook...")
      self.book = tempBook   #if there is any problem loading the new file, we want to continue working with the previous one
    except IOError:                  #this catches the error for non existing files
      print("Error: unable to load '%s'" % filename)
      print("Loading previous birthdaybook...")
      self.book = tempBook   #revert back to old birthdaybook
      
            
def main(): #main method is where the program will start, and handle the command line interface entry. We create and modify objects in this method, through the methods of the other classes 
  print('________________________________________________________________________________________________________________________')
  print('1. help -- bring up this help menu for commands')
  print('2. add -- add someone to the birthday book using the format add first(string) last(string) month(int) day(int) year(int)')
  print('3. delete -- delete someone from the birthday book using the format delete number(int)')
  print('4. list -- list all entries in the birthday book using the keyword list with no arguments')
  print('5. search -- search for an entry in the birthday book using the first or last name (**not case sensitive)')
  print('6. save -- save birthday book to a file specified by the user. format save filename.txt')
  print('7. load -- loads the birthdays from a file specified by the user into the program. format load filename.txt')
  print('8. quit -- quit the program with keyword quit with no arguments')
  running = True                  
  bdayBook = BirthdayBook()   #create an initial birthdaybook object to work with
  while running == True:      #keep accepting commands until running = False (set in quit)
    entry = input()
    entry = entry.split()     #split up the users entry into arguments
    command = entry[0]  
    if command == 'add':
      try:
        bdayBook.add(Person(entry[1], entry[2], entry[3], entry[4], entry[5])) #we can create a new person object without assigning it to a variable, since we only want to do this once, and it doesnt have to be modified ever
        print('Added: "' + entry[1] + ' ' + entry[2] + ', ' + entry[3] + '/' + entry[4] + '/' + entry[5] + '"')
      except IndexError:   #if there is an incorrect number of arguments, entry will not have 5 fields and will have an IndexError, which we deal with here
        print('Unable to add to birthdaybook, correct format is "add firstname lastname month day year"')
    elif command == 'list':
      bdayBook.list()
    elif command == 'delete':
      bdayBook.delete(entry[1])
    elif command == 'save':
      bdayBook.save(entry[1])
    elif command == 'load':
      bdayBook.load(entry[1])
    elif command == 'quit':
      print('Quitting Program')
      running = False           #while loop stops running after this boolean is flipped
    elif command == 'help':
      print('________________________________________________________________________________________________________________________')
      print('1. help -- bring up this help menu for commands')
      print('2. add -- add someone to the birthday book using the format add first(string) last(string) month(int) day(int) year(int)')
      print('3. delete -- delete someone from the birthday book using the format delete number(int)')
      print('4. list -- list all entries in the birthday book using the keyword list with no arguments')
      print('5. search -- search for an entry in the birthday book using the first or last name (**not case sensitive)')
      print('6. save -- save birthday book to a file specified by the user. format save filename.txt')
      print('7. load -- loads the birthdays from a file specified by the user into the program. format load filename.txt')
      print('8. quit -- quit the program with keyword quit with no arguments')
    elif command == 'search':
      bdayBook.search(entry[1])
    else:
      print("Please enter a valid command. Type 'help' for a list of commands")
  sys.exit()     #close the program when it stops running, so it cant accept any more commands
  
if __name__ == '__main__': #make sure we call the main method to start the program
  main()