import enum

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time, Text, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DifficultyEnum(enum.Enum):
    easy = 1
    easy_medium = 2
    medium = 3
    medium_hard = 4
    hard = 5


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    creation_date = Column(Date)
    last_access_date = Column(Date)

    Recipes = relationship("Recipe")


# @jew4731's stab at creating a table. Need constraints
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    servings = Column(Integer)
    cook_time = Column(Time)
    name = Column(String)
    description = Column(Text)
    difficulty = Column(Enum(DifficultyEnum))

    Steps = relationship("Step")
    Ingredients = relationship("RecipeIngredients")

class Category(Base):
    __tablename__ = "categories"

    category_type = Column(String, primary_key=True)  # String bc users can make them
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)


class Step(Base):
    __tablename__ = "steps"

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    step_nr = Column(Integer, primary_key=True)
    instruction = Column(Text)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    aisle = Column(String)
    name = Column(String)


class CookedBy(Base):
    __tablename__ = "cookedby"

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    rating = Column(Integer)  # uncertain what type this should be
    scale = Column(Float)  # Scale can be INT or FLOAT; float seems better
    cook_date = Column(Date, nullable=False)


class RecipeIngredients(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    amount = Column(Float, nullable=False)  # float or integer?

    Ingredient = relationship("Ingredient")


class UserPantry(Base):
    __tablename__ = "pantry"

    pantry_item_id = Column(Integer, primary_key=True)  # for storing more than one of each ingredient
    # ^ not required, will make execution of CookedBy slightly more difficult
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    expiration_date = Column(Date)
    purchase_date = Column(Date)
    quantity_bought = Column(Float)  # not required
    current_quantity = Column(Float)  # scale can be float, so this must be as well

    ingredient = relationship("Ingredient", back_populates="pantry")
