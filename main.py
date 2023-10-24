# 
# Name: Rimsha Rizvi
# Project: MovieLens Application
# Uses MovieLens database and N-tier design to install a menu based system which allows user to retrieve information about movie(s) and/or update information for them.
#

import sqlite3
import objecttier

##################################################################  
#
# print_stats
#
# Given a connection to the MovieLens database, executes various SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
  print("General stats:")
  num = objecttier.num_movies(dbConn)
  print("  # of movies:",f"{num:,}")
  num_ratings = objecttier.num_reviews(dbConn)
  print("  # of reviews:",f"{num_ratings:,}")


##################################################################  
#
# command1
#
# calls get_movies = get's movie ID, title and year of release from user input movie name
#
def command1(dbConn):
  print()
  name = input("Enter movie name (wildcards _ and % supported): ")
  movie = objecttier.get_movies(dbConn, name)
  print()
  if movie is None:  # error
    print("# of movies found: 0")
  elif len(movie) == 0:  # no movie in database
    print("# of movies found: 0")
  elif len(movie) > 100:  # more than 100 movies found
    print("# of movies found:", len(movie))
    print()
    print("There are too many movies to display, please narrow your search and try again...")
  else:
    print("# of movies found:", len(movie))
    print()
    for s in movie:
      print(s._Movie_ID, ":", s._Title, "("+str(s._Release_Year)+")")


##################################################################  
#
# command2
#
# calls get_movie_details = get's detailed information about the movie from the user input movie id
#
def command2(dbConn):
  print()
  id = input("Enter movie id: ")
  
  details = objecttier.get_movie_details(dbConn, id)
  print()
  if details is None:  # error or if object has no movie
      print("No such movie...")
  else:
    print(details._Movie_ID, ":", details._Title)
    print("  Release date:", details._Release_Date)
    print("  Runtime:", details._Runtime, "(mins)") 
    print("  Orig language:", details._Original_Language)
    print("  Budget: $"+ f"{details._Budget:,}", "(USD)")
    print("  Revenue: $"+ f"{details._Revenue:,}", "(USD)")
    print("  Num reviews:", details._Num_Reviews)
    print("  Avg rating:", f"{details._Avg_Rating:.2f}","(0..10)")
    
    print("  Genres:", end =' ')

    for i in range(0,len(details._Genres)):
      print(details._Genres[i]+",", end = ' ')
    print()

    print("  Production companies:", end =' ')

    for i in range(0,len(details._Production_Companies)):
      print(details._Production_Companies[i]+",", end = ' ')
    print()
    
    print("  Tagline:",details._Tagline)


##################################################################  
#
# command3
#
# calls get_top_N_movies = retrieves and outputs top N movies based on their average rating from user inputs N and minimum number of reviews
#
def command3(dbConn):
  print()
  n = int(input("N? "))
  if n < 1:
    print("Please enter a positive value for N...")
  else:  # ensures positive N
    min = int(input("min number of reviews? "))
    if min < 1:
      print("Please enter a positive value for min number of reviews...")
    else:  # ensures positive min no. of reviews
      topmovie = objecttier.get_top_N_movies(dbConn, n, min)
      print()
    
      if topmovie is None or topmovie == []:  # if error or empty
          pass
      else:
          for s in topmovie:
            print(s._Movie_ID, ":", s._Title, "("+str(s._Release_Year)+ ")"+ ", avg rating =", f"{s._Avg_Rating:.2f}", "("+str(s._Num_Reviews)+" reviews)")


##################################################################  
#
# command4
#
# calls add_review = inserts a new review for a movie into the database
#
def command4(dbConn):
  print()
  rating = int(input("Enter rating (0..10): "))
  if rating < 0 or rating > 10:  # valid rating?
    print("Invalid rating...")
  else:
    id = int(input("Enter movie id: "))
    print()
    insert = objecttier.add_review(dbConn, id, rating)
    if insert == 0:
      print("No such movie...")
    else:
      print("Review successfully inserted")


##################################################################  
#
# command5
#
# calls set_tagline = for a given movie, it either inserts a tagline (if not there already) or updates the tagline (if there already)
#
def command5(dbConn):
  print()
  tagline = input("tagline? ")
  id = int(input("movie id? "))
  set = objecttier.set_tagline(dbConn, id, tagline)
  print()
  if set == 0:  # if unsuccessful
    print("No such movie...")
  else:
    print("Tagline successfully set")
  

##################################################################  
#
# main
#
print('** Welcome to the MovieLens app **')

dbConn = sqlite3.connect('MovieLens.db')

print()

print_stats(dbConn)

print()

inp = input('Please enter a command (1-5, x to exit): ')
# menu system
while (inp != "x"):
  if inp == "1":
    command1(dbConn)
  elif inp == "2":
    command2(dbConn)
  elif inp == "3":
    command3(dbConn)
  elif inp == "4":
    command4(dbConn)
  elif inp == "5":
    command5(dbConn)
  else:
    print("**Error, unknown command, try again...")

  print()
  inp = input('Please enter a command (1-5, x to exit): ')

#
# done
#