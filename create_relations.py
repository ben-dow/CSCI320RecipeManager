Python 3.6.2 (v3.6.2:5fd33b5, Jul  8 2017, 04:14:34) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
categories = Table('user', metadata,
    Column('Category_Type', Integer, nullable=False, primary_key=True),
    Column('recipeID', BigInt, ForeignKey(“recipes.recipeID), nullable=False)
)

recipes = Table('recipes', metadata,
    Column('recipeID', BigInteger, nullable=False, unique=True, primary_key=True),
    Column('cookTime', Integer, nullable=False),
    Column('name', String(40), nullable=False),
    Column('description', Text, nullable=False),
    Column(‘Servings’, Integer, nullable=False),
    Column(‘Difficulty’, ENUM, nullable=False),
    Column(‘steps’, Integer, nullable=False)

)

ingredients = Table(‘ingredients’, metadata,
	Column(‘IngredientID’, Integer, nullable=False, unique=True, primary_key=True ),
	Column(‘name’, String(30), nullable=false),
	Column(‘Aisle’, String(30)),
)
user = Table(‘user’, metadata,
	Column(‘userID’, BigInt, nullable=False, unique=True, primary_key=True),
	Column(‘username’, String(30), nullable=False, unique=True),
	Column(‘creation_date’, Time, nullable=False),
	Column(‘password’, String(20), nullable=False),
Column(‘last_access_date’, DateTime, nullable=False, onupdate=datetime.datetime.now),
)

userPantry = Table(‘userPantry’, metadata,
	Column(‘pantryItemID’, Integer, unique=True, primary_key=True),
	Column(‘ingredientID’, Integer, ForeignKey(“Ingredients.IngredientID”),
	Column(‘userID’, BigInt, ForeignKey(“User.userID”), nullable=False),
	Column(‘expirationDate’, Time, nullable=True),
	Column(‘purchaseDate’, Time, nullable=True),
	Column(‘currentQuantity’, Float, nullable=False, default=0),
	Column(‘quantityBought’, Float, nullable=False, default=0),
)
Recipe_ingredient = Table(‘recipe_ingredient’, metadata,
Column(‘recipeID’, BigInt, ForeignKey(“recipes.recipeID”), nullable=False, primary_key=True),
Column(‘IngredientID’, Integer, ForeignKey(“Ingredients.IngredientID”), nullable=False, primary_key=True),
	Column(‘Amount’, Float, nullable=False)
)
cookedBy = Table(‘cookedBy’, metadata,
Column(“recipeID”, BigInt, Foreign_Key(“recipes.recipeID”), nullable=False, primary_key=True),
Column(‘userID’, BigInt, Foreign_Key(“User.userID”), nullable=False, primary_key=True),
	Column(‘Rating’, Integer, nullable=False),
	Column(‘Scale’, Float, nullable=False),
	Column(‘cookDate,’ Time),
)
Steps = Table(‘steps’, metadata,
Column(‘recipeID’, BigInt, Foreign_Key(“recipes.recipeID”), nullable=False, primary_key=True),
	Column(‘Stepnr’, Integer, primary_key=True),
	Column(‘Instructions’,Text, nullable=False),
)
