 #
# File: objecttier.py
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
# Modified by: Rimsha Rizvi
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, id, name, year):
    self._Movie_ID = id;
    self._Title = name;
    self._Release_Year = year;

  @property  # to ensure not read only
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, id, name, year, num, avg):
    self._Movie_ID = id;
    self._Title = name;
    self._Release_Year = year;
    self._Num_Reviews = num;
    self._Avg_Rating = avg;

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, movie_id, title, release_date, runtime, original_language, budget, revenue, num_reviews, avg_rating, tagline):
    self._Movie_ID = movie_id;
    self._Title = title;
    self._Release_Date = release_date;
    self._Runtime = runtime;
    self._Original_Language = original_language;
    self._Budget = budget;
    self._Revenue = revenue;
    self._Num_Reviews = num_reviews;
    self._Avg_Rating = avg_rating;
    self._Tagline = tagline;
    self._Genres = [];  # genre is list as it holds many values
    self._Production_Companies = [];  # Production_Companies is list as it holds many values

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title
  
  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime
  
  @property
  def Original_Language(self):
    return self._Original_Language
  
  @property
  def Budget(self):
    return self._Budget
  
  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating
  
  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies

##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  try:
    sql = "select count(*) from movies;"
    executeRow = datatier.select_one_row(dbConn, sql, [])[0]
    return executeRow
  except Exception as err:
       print("num_movies failed:", err)
       return -1
    

##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  try:
    sql = "select count(*) from ratings;"
    executeRow = datatier.select_n_rows(dbConn, sql, [])[0][0]
    return executeRow
  except Exception as err:
       print("num_movies failed:", err)
       return -1


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  try:
    sql = "select movie_id, title, strftime('%Y', release_date) from Movies where title like ? order by title"
    executeRow = datatier.select_n_rows(dbConn, sql, [pattern])

    result = []
    if executeRow == None:  # if no movies in data det like pattern
      return result
    
    for row in executeRow:
      id = row[0]
      name = row[1]
      year = row[2]
      result.append(Movie(id, name, year))
      
    return result
  except Exception as err:
       print("get_movies failed:", err)
       return []


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  # sql for movie objects and its properties
  sql = "select movies.movie_id, title, date(release_date), runtime, original_language, budget, revenue, count(ratings.rating), avg(ratings.rating), Movie_Taglines.tagline from Movies left join Ratings on movies.movie_id = ratings.movie_id left join Movie_Taglines on movies.movie_id = movie_taglines.movie_id where movies.movie_id = ? group by movies.movie_id order by movies.movie_id"

  executeRow = datatier.select_one_row(dbConn, sql, [movie_id])

  # sql for genre objects and its properties
  genre_sql = "select genre_name from movie_genres join genres on movie_genres.genre_id = genres.genre_id where movie_id = ? order by genre_name"
  executeRow2 = datatier.select_n_rows(dbConn, genre_sql, [movie_id])

  # sql for production objects and its properties
  production_sql = "select Company_Name from Movie_Production_Companies join Companies on Movie_Production_Companies.Company_ID = Companies.Company_ID where Movie_ID = ? order by Company_Name"
  executeRow3 = datatier.select_n_rows(dbConn, production_sql, [movie_id])


  if executeRow == None:
    return None
  elif executeRow == ():
    return None

  id = executeRow[0]
  name = executeRow[1]
  date = executeRow[2]
  runtime = executeRow[3]
  original_language = executeRow[4]
  budget = executeRow[5]
  revenue = executeRow[6]
  num_reviews = executeRow[7]
  avg_rating = executeRow[8]
  tag = executeRow[9]

  if avg_rating == None:  # if no rating
    avg_rating = 0

  if tag == None:  # if no tagline
    tag = ""  # empty string instead of None

  if num_reviews == None:  # if no # reviews 
    num_reviews = 0

  result = MovieDetails(id, name, date, runtime, original_language, budget, revenue, num_reviews, avg_rating, tag)

  if executeRow2 == None:  # if no genre
    pass
  else:
    for genre in executeRow2:  # add genre in list
      result._Genres.append(genre[0])

  if executeRow3 == None:  # if no movie production companies
    pass
  else:
    for pc in executeRow3:    # add movie production companies in list
      result._Production_Companies.append(pc[0])
    
  return result
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  try:
    sql = "select movies.movie_id, movies.title, strftime('%Y', movies.release_date), count(ratings.rating), avg(ratings.rating) from movies join ratings on movies.movie_id = ratings.movie_id group by movies.movie_id having count(ratings.rating) >= ? order by avg(ratings.rating) desc limit ?;"

    
    executeRow = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
    result = []
    if executeRow == None:
      return result
    
    for row in executeRow:
      id = row[0]
      name = row[1]
      year = row[2]
      num = row[3]
      avg = row[4]
      result.append(MovieRating(id, name, year, num, avg))
    return result
  except Exception as err:
       print("get_top_N_movies failed:", err)
       return []


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  try:
    sql = "select movie_id from movies where movie_id = ?"
    executeRow = datatier.select_one_row(dbConn, sql, [movie_id])

    if executeRow == None or executeRow == () :
      return 0
    else:
      sql2 = "insert into ratings(movie_id, rating) values (?,?);"
      executeRow2 = datatier.perform_action(dbConn, sql2, [movie_id, rating])

      if executeRow2 != -1:  # ensures perform action doesn't failed
        return 1
      return 0
      
  except:
    return 0


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  try:
    sql = "select movie_id from movies where movie_id = ?"
    executeRow = datatier.select_one_row(dbConn, sql, [movie_id])

    if executeRow == None:
      return 0
    if executeRow == ():
      return 0

    sql2 = "select tagline from movie_taglines where movie_id = ?"
    executeRow2 = datatier.select_one_row(dbConn, sql2, [movie_id])
    

    if not executeRow2:  # does tagline not exist in database
      sql3 = "insert into movie_taglines(movie_id, tagline) values (?,?);"
      add = datatier.perform_action(dbConn, sql3, [movie_id, tagline])

      if add != -1:  # ensures perform action doesn't fail
        return 1
      else:
        return 0
    
    else:  # tagline already exists
      sql4 = "update movie_taglines set tagline = ? where movie_id = ?;"
      add2 = datatier.perform_action(dbConn, sql4, [tagline, movie_id])

      if add2 == -1:
        return 0
      else:
        return 1   
  except:
    return 0
